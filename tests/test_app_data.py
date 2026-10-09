"""Checks on the committed app_data/ files: export schema, geo coverage, metrics, app smoke test."""

import json
import pathlib
import sys

import pandas as pd
import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_DATA = ROOT / "app_data"
sys.path.insert(0, str(ROOT / "src"))

pytestmark = pytest.mark.skipif(not (APP_DATA / "meta.json").exists(), reason="app_data not exported")

EXPECTED_REGIONS = {"planning_room": 542, "district_area": 143, "prediction_area": 58}


def _table(name):
    return pd.read_parquet(APP_DATA / f"{name}.parquet")


@pytest.mark.parametrize("level,count", EXPECTED_REGIONS.items())
def test_every_region_has_a_polygon(level, count):
    geo = json.loads((APP_DATA / "geo" / f"lor_{level}.geojson").read_text(encoding="utf-8"))
    geo_ids = {f["properties"]["region_id"] for f in geo["features"]}
    regional = _table("timegoal_region_yearly")
    ids = set(regional.loc[regional["region_level"] == level, "region_id"])
    assert len(geo_ids) == count
    assert ids == geo_ids


def test_regional_quotes_are_probabilities():
    q = _table("timegoal_region_yearly")["ems_critical_timegoal_quote"].dropna()
    assert q.between(0, 1).all()


def test_monthly_export_is_consistent():
    m = _table("missions_monthly")
    assert (m["mission_count_within_timegoal"] <= m["mission_count_with_response_time"]).all()
    assert (m["mission_count_with_response_time"] <= m["mission_count"]).all()
    assert not m.duplicated(["mission_month", "district_code", "mission_group", "criticality_tier"]).any()


def test_complete_months_drops_partial_month():
    from utils import metrics

    m = pd.DataFrame({"mission_month": pd.to_datetime(["2026-08-01", "2026-09-01", "2026-10-01"])})
    assert len(metrics.complete_months(m, "2026-10-07")) == 2
    assert len(metrics.complete_months(m, "2026-10-31")) == 3


def test_official_kpis_citywide_year():
    from utils import metrics

    k = metrics.official_kpis(_table("timegoal_region_yearly"), 2025)
    assert 0.3 < k["quote"] < 0.9
    assert k["computed"] > 0


@pytest.mark.parametrize("level_label", ["Bezirksregion (143)", "Planungsraum (542)", "Prognoseraum (58)"])
def test_app_renders_for_every_map_level(level_label):
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "src" / "app.py"), default_timeout=60).run()
    assert not at.exception
    at.radio[0].set_value(level_label).run()
    assert not at.exception
    assert len(at.metric) == 4
