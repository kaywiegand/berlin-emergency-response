"""Ingest Berliner Feuerwehr Open Data into DuckDB (raw layer, all columns VARCHAR).

Modes:
  default   current year of Mission/Regional data, daily series, turnout snapshot
  --full    all years from --first-year to --last-year, all turnout quarters
  --years   explicit years (Mission, Regional >= 2024, Turnout quarters)

Each source file maps to one partition of a raw table. A run downloads and
validates everything first, then replaces all affected partitions in a single
transaction: reruns are idempotent and a failure leaves the database untouched.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import pathlib
import sys
from dataclasses import dataclass

import duckdb
import httpx

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DB = BASE_DIR / "data" / "berlin_emergency.duckdb"
DEFAULT_RAW_DIR = BASE_DIR / "data" / "raw"
DEFAULT_BASE_URL = (
    "https://raw.githubusercontent.com/Berliner-Feuerwehr/BF-Open-Data/main/Datasets"
)

FIRST_MISSION_YEAR = 2018
FIRST_REGIONAL_YEAR = 2024
QUARTERS = ("q1", "q2", "q3", "q4")

MISSION_COLUMNS = [
    "mission_date", "mission_type", "dispatchcode_category",
    "dispatchcode_category_name", "dispatchcode_criticality",
    "mission_location_district", "response_time", "units_non_berlin_involed",
    "units_several_involved", "units_reinforcements_called", "units_organisations",
    "firstresponder_alarmed", "firstresponder_indication",
    "firstresponder_first_arrival", "units_first_type", "emergency_doctor_involved",
]  # fmt: skip

_STATS = [
    "mission_count_all", "mission_count_ems", "mission_count_ems_critical",
    "mission_count_ems_critical_cpr", "mission_count_fire",
    "mission_count_technical_rescue",
]  # fmt: skip
_RESPONSE = [
    f"response_time_{kind}_{stat}"
    for kind in (
        "ems_critical", "ems_critical_cpr", "fire_time_to_first_pump",
        "fire_time_to_first_ladder", "fire_time_to_full_crew", "technical_rescue",
    )
    for stat in ("mean", "median", "std")
]  # fmt: skip
_TIMEGOAL = [
    "mission_count_ems_critical_timegoal_computed",
    "mission_count_fire_timegoal_computed",
    "mission_count_ems_critical_timegoal_reached",
    "mission_count_fire_timegoal_reached",
]

REGIONAL_METRICS = _STATS + _TIMEGOAL + _RESPONSE
DAILY_COLUMNS = (
    ["mission_created_date"]
    + _STATS
    + [f"mission_count_rd{i}" for i in range(1, 6)]
    + _RESPONSE
)
TURNOUT_COLUMNS = [
    "wache_nummer",
    *[
        f"{prefix}_{unit}"
        for unit in ("RTW", "NEF", "LHF", "DLK", "ELW")
        for prefix in ("anzahl_alarmierungen", "mittlere_ausrueckedauer")
    ],
    "wache_name", "start_date", "end_date",
]  # fmt: skip

META_COLUMNS = ["_partition", "_source_file", "_loaded_at"]


@dataclass(frozen=True)
class Unit:
    """One source file and the raw-table partition it replaces."""

    table: str
    partition: str
    path: str
    columns: tuple[str, ...]

    @property
    def filename(self) -> str:
        return self.path.rsplit("/", 1)[-1]


def mission_unit(year: int) -> Unit:
    return Unit(
        "raw_mission_data", str(year),
        f"Mission_Data/mission_data_set_open_data_{year}.csv",
        tuple(MISSION_COLUMNS),
    )  # fmt: skip


def regional_units(year: int) -> list[Unit]:
    levels = {
        "raw_regional_planning_room": ("planning_room", "planning_room_id", "planning_room_name"),
        "raw_regional_district_area": ("district_area", "district_area_id", "district_area_name"),
        "raw_regional_prediction_area": ("prediction_area", "prediction_area_id", "prediction_area_name"),
    }  # fmt: skip
    return [
        Unit(
            table, str(year),
            f"Regional_Data/{year}/BFw_{level}_data_{year}.csv",
            (id_col, name_col, *REGIONAL_METRICS),
        )
        for table, (level, id_col, name_col) in levels.items()
    ]  # fmt: skip


def daily_unit() -> Unit:
    return Unit(
        "raw_daily_mission_data", "all",
        "Daily_Data/BFw_mission_data_daily.csv", tuple(DAILY_COLUMNS),
    )  # fmt: skip


def turnout_unit(period: str) -> Unit:
    return Unit(
        "raw_turnout_times", period,
        f"Turnout_Times/crew_turnout_times_{period}.csv", tuple(TURNOUT_COLUMNS),
    )  # fmt: skip


def plan_units(
    full: bool, years: list[int] | None, first_year: int, last_year: int
) -> list[Unit]:
    if years:
        selected = sorted(set(years))
    elif full:
        selected = list(range(first_year, last_year + 1))
    else:
        selected = [last_year]

    units = [mission_unit(y) for y in selected]
    for y in selected:
        if y >= FIRST_REGIONAL_YEAR:
            units += regional_units(y)
    units.append(daily_unit())
    if full or years:
        units += [turnout_unit(f"{y}_{q}") for y in selected for q in QUARTERS]
    units.append(turnout_unit("current"))
    return units


def download(client: httpx.Client, url: str, dest: pathlib.Path) -> None:
    """Stream url to dest atomically; any HTTP error or empty body is fatal."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_suffix(dest.suffix + ".part")
    try:
        with client.stream("GET", url) as response:
            response.raise_for_status()
            with part.open("wb") as fh:
                for chunk in response.iter_bytes(1 << 20):
                    fh.write(chunk)
    except (httpx.HTTPError, OSError) as exc:
        part.unlink(missing_ok=True)
        raise SystemExit(f"download failed: {url} ({exc})") from exc
    if part.stat().st_size == 0:
        part.unlink()
        raise SystemExit(f"empty file: {url}")
    part.replace(dest)


def read_header(path: pathlib.Path) -> list[str]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        return next(csv.reader(fh), [])


def validate_header(unit: Unit, header: list[str]) -> list[str]:
    """Return the file's column names (unnamed index column renamed to _index)."""
    names = ["_index" if i == 0 and not h.strip() else h.strip() for i, h in enumerate(header)]
    missing = [c for c in unit.columns if c not in names]
    if missing:
        raise SystemExit(f"{unit.filename}: missing columns {missing}")
    extra = [c for c in names if c not in unit.columns and c != "_index"]
    if extra:
        print(f"  warn  {unit.filename}: ignoring new columns {extra}")
    return names


def ensure_table(con: duckdb.DuckDBPyConnection, unit: Unit) -> None:
    cols = ", ".join(f'"{c}" VARCHAR' for c in unit.columns)
    con.execute(
        f"CREATE TABLE IF NOT EXISTS {unit.table} ({cols}, "
        "_partition VARCHAR, _source_file VARCHAR, _loaded_at TIMESTAMP)"
    )


def load_unit(
    con: duckdb.DuckDBPyConnection,
    unit: Unit,
    path: pathlib.Path,
    names: list[str],
    loaded_at: dt.datetime,
) -> int:
    ensure_table(con, unit)
    con.execute(f"DELETE FROM {unit.table} WHERE _partition = ?", [unit.partition])
    select = ", ".join(f'"{c}"' for c in unit.columns)
    con.execute(
        f"INSERT INTO {unit.table} "
        f"SELECT {select}, ?, ?, ? FROM read_csv(?, header=true, all_varchar=true, names=?)",
        [unit.partition, unit.filename, loaded_at, str(path), names],
    )
    (rows,) = con.execute(
        f"SELECT count(*) FROM {unit.table} WHERE _partition = ?", [unit.partition]
    ).fetchone()
    if rows == 0:
        raise SystemExit(f"{unit.filename}: no data rows")
    return rows


def run(args: argparse.Namespace) -> None:
    units = plan_units(args.full, args.years, args.first_year, args.last_year)
    raw_dir = pathlib.Path(args.raw_dir)
    base_url = args.base_url.rstrip("/")
    print(f"{len(units)} source files -> {args.db}")

    prepared: list[tuple[Unit, pathlib.Path, list[str]]] = []
    transport = httpx.HTTPTransport(retries=3)
    with httpx.Client(follow_redirects=True, timeout=120.0, transport=transport) as client:
        for unit in units:
            dest = raw_dir / unit.path
            print(f"  fetch {unit.path}")
            download(client, f"{base_url}/{unit.path}", dest)
            prepared.append((unit, dest, validate_header(unit, read_header(dest))))

    db_path = pathlib.Path(args.db)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    loaded_at = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None)
    con = duckdb.connect(str(db_path))
    try:
        con.execute("BEGIN")
        for unit, path, names in prepared:
            rows = load_unit(con, unit, path, names, loaded_at)
            print(f"  load  {unit.table}[{unit.partition}] {rows} rows")
        con.execute("COMMIT")
    except BaseException:
        con.execute("ROLLBACK")
        raise
    finally:
        con.close()


def build_parser() -> argparse.ArgumentParser:
    today_year = dt.date.today().year
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--full", action="store_true", help="load all years and turnout quarters")
    p.add_argument("--years", type=int, nargs="+", help="load only these years")
    p.add_argument("--first-year", type=int, default=FIRST_MISSION_YEAR)
    p.add_argument("--last-year", type=int, default=today_year)
    p.add_argument("--base-url", default=DEFAULT_BASE_URL)
    p.add_argument("--db", default=str(DEFAULT_DB))
    p.add_argument("--raw-dir", default=str(DEFAULT_RAW_DIR))
    return p


if __name__ == "__main__":
    run(build_parser().parse_args())
    sys.exit(0)
