import duckdb
import pytest

from conftest import YEARS, ingest


def _args(tmp_path, base_url, *extra):
    parser = ingest.build_parser()
    return parser.parse_args(
        [
            "--base-url", base_url,
            "--db", str(tmp_path / "t.duckdb"),
            "--raw-dir", str(tmp_path / "raw"),
            "--first-year", str(YEARS[0]),
            "--last-year", str(YEARS[-1]),
            *extra,
        ]
    )  # fmt: skip


def _count(tmp_path, table, where="true"):
    con = duckdb.connect(str(tmp_path / "t.duckdb"), read_only=True)
    try:
        return con.execute(f"select count(*) from {table} where {where}").fetchone()[0]
    finally:
        con.close()


def test_full_load_is_idempotent(upstream, tmp_path):
    _, url = upstream
    for _ in range(2):
        ingest.run(_args(tmp_path, url, "--full"))
    assert _count(tmp_path, "raw_mission_data") == 4
    assert _count(tmp_path, "raw_mission_data", "_partition = '2026'") == 2
    assert _count(tmp_path, "raw_regional_planning_room") == 4
    assert _count(tmp_path, "raw_daily_mission_data") == 2
    assert _count(tmp_path, "raw_turnout_times") == 2 * 4 * 2 + 2


def test_default_mode_replaces_only_current_year(upstream, tmp_path):
    _, url = upstream
    ingest.run(_args(tmp_path, url, "--full"))
    ingest.run(_args(tmp_path, url))
    assert _count(tmp_path, "raw_mission_data", "_partition = '2025'") == 2
    assert _count(tmp_path, "raw_mission_data") == 4


def test_broken_url_aborts_without_touching_db(upstream, tmp_path):
    root, url = upstream
    ingest.run(_args(tmp_path, url, "--full"))
    (root / ingest.mission_unit(2026).path).unlink()
    with pytest.raises(SystemExit, match="download failed"):
        ingest.run(_args(tmp_path, url, "--full"))
    assert _count(tmp_path, "raw_mission_data") == 4


def test_missing_column_aborts(upstream, tmp_path):
    root, url = upstream
    path = root / ingest.daily_unit().path
    path.write_text(path.read_text().replace("mission_count_rd3", "renamed"))
    with pytest.raises(SystemExit, match="missing columns"):
        ingest.run(_args(tmp_path, url))


def test_empty_file_aborts(upstream, tmp_path):
    root, url = upstream
    (root / ingest.daily_unit().path).write_text("")
    with pytest.raises(SystemExit, match="empty file"):
        ingest.run(_args(tmp_path, url))
