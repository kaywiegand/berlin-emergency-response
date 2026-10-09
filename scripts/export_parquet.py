"""Export dbt marts to app_data/*.parquet: the only data the Streamlit app reads.

Monthly grain for missions keeps the committed files small (the daily bot commit in CI
rewrites them); medians are not additive, so the export carries response-time sums instead.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib

import duckdb

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DB = BASE_DIR / "data" / "berlin_emergency.duckdb"
DEFAULT_OUT = BASE_DIR / "app_data"

EXPORTS = {
    "districts": "select district_code, district_name, district_short from dim_district order by 1",
    "timegoal_region_yearly": """
        select f.region_level, f.region_id, r.region_name, r.district_code, d.district_name,
               r.district_area_id, r.prediction_area_id, f.data_year,
               f.mission_count_all, f.mission_count_ems, f.mission_count_ems_critical,
               f.ems_critical_timegoal_computed, f.ems_critical_timegoal_reached,
               f.ems_critical_timegoal_quote, f.response_time_ems_critical_mean,
               f.response_time_ems_critical_median
        from fct_timegoal_region_yearly f
        join dim_region r on f.region_level = r.region_level and f.region_id = r.region_id
        join dim_district d on r.district_code = d.district_code
        order by f.region_level, f.region_id, f.data_year""",
    "missions_monthly": """
        select date_trunc('month', f.mission_date)::date as mission_month,
               f.district_code, d.district_name, f.mission_group, f.criticality_tier,
               sum(f.mission_count)::bigint as mission_count,
               sum(f.mission_count_with_response_time)::bigint as mission_count_with_response_time,
               sum(f.mission_count_within_timegoal)::bigint as mission_count_within_timegoal,
               sum(f.response_time_mean_seconds * f.mission_count_with_response_time)
                   as response_time_sum_seconds
        from fct_missions_daily_district f
        join dim_district d on f.district_code = d.district_code
        group by 1, 2, 3, 4, 5
        order by 1, 2, 4, 5""",
    "missions_daily_citywide": "select * exclude (loaded_at) from fct_missions_daily_citywide order by mission_date",
    "turnout_quarterly": "select * exclude (loaded_at) from fct_turnout_times_quarterly order by period_start, station_id",
    "events": "select * from seed_events order by event_id",
}


def export(db: pathlib.Path, out_dir: pathlib.Path) -> dict[str, int]:
    out_dir.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db), read_only=True)
    try:
        counts = {}
        for name, query in EXPORTS.items():
            path = out_dir / f"{name}.parquet"
            con.execute(f"copy ({query}) to '{path}' (format parquet, compression zstd)")
            counts[name] = con.execute(f"select count(*) from '{path}'").fetchone()[0]
            if counts[name] == 0:
                raise SystemExit(f"{name}: export is empty")
        (data_through,) = con.execute("select max(mission_date) from fct_missions_daily_citywide").fetchone()
    finally:
        con.close()
    meta = {
        "data_through": data_through.isoformat(),
        "exported_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    for name, rows in export(pathlib.Path(args.db), pathlib.Path(args.out_dir)).items():
        print(f"{name}: {rows} rows")


if __name__ == "__main__":
    main()
