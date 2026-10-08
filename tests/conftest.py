"""Fixture server: serves tiny CSVs in the upstream BF-Open-Data layout."""

import functools
import http.server
import importlib.util
import pathlib
import sys
import threading

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("ingest", ROOT / "scripts" / "ingest.py")
ingest = importlib.util.module_from_spec(_spec)
sys.modules["ingest"] = ingest
_spec.loader.exec_module(ingest)

YEARS = (2025, 2026)


def _write(root: pathlib.Path, unit: "ingest.Unit", rows: int = 2, index: bool = False) -> None:
    path = root / unit.path
    path.parent.mkdir(parents=True, exist_ok=True)
    header = (["" ] if index else []) + list(unit.columns)
    lines = [",".join(header)]
    for i in range(rows):
        values = [f"{i}-{c}" for c in unit.columns]
        lines.append(",".join(([str(i)] if index else []) + values))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.fixture
def upstream(tmp_path):
    root = tmp_path / "upstream"
    for year in YEARS:
        _write(root, ingest.mission_unit(year), index=True)
        for unit in ingest.regional_units(year):
            _write(root, unit)
        for q in ingest.QUARTERS:
            _write(root, ingest.turnout_unit(f"{year}_{q}"))
    _write(root, ingest.daily_unit())
    _write(root, ingest.turnout_unit("current"), index=True)

    handler = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=str(root)
    )
    handler.log_message = lambda *a, **k: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield root, f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
