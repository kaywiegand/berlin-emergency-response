"""Pure aggregation functions behind the dashboard (no Streamlit, unit-testable)."""

from __future__ import annotations

import pandas as pd

OFFICIAL_LEVEL = "district_area"  # all three Regional_Data levels sum to the same totals
TIERS = ["A", "B", "C", "D", "E", "O", "unknown"]
DEFAULT_TIERS = ["D", "E"]


def official_kpis(regional: pd.DataFrame, year: int) -> dict:
    """City-wide official Hilfsfrist figures for one year."""
    d = regional[(regional["region_level"] == OFFICIAL_LEVEL) & (regional["data_year"] == year)]
    computed = d["ems_critical_timegoal_computed"].sum()
    reached = d["ems_critical_timegoal_reached"].sum()
    critical = d["mission_count_ems_critical"].sum()
    weighted_mean = (
        (d["response_time_ems_critical_mean"] * d["mission_count_ems_critical"]).sum() / critical
        if critical
        else float("nan")
    )
    return {
        "quote": reached / computed if computed else float("nan"),
        "computed": int(computed),
        "mean_response_seconds": weighted_mean,
        "missions": int(d["mission_count_all"].sum()),
    }


def official_by_district(regional: pd.DataFrame, year: int) -> pd.DataFrame:
    d = regional[(regional["region_level"] == OFFICIAL_LEVEL) & (regional["data_year"] == year)]
    g = d.groupby("district_name", as_index=False)[
        ["ems_critical_timegoal_computed", "ems_critical_timegoal_reached"]
    ].sum()
    g["share"] = g["ems_critical_timegoal_reached"] / g["ems_critical_timegoal_computed"]
    return g[["district_name", "share"]]


def complete_months(monthly: pd.DataFrame, data_through: str) -> pd.DataFrame:
    """Drop the last month if the data does not reach its final day."""
    through = pd.Timestamp(data_through)
    cutoff = through.to_period("M").start_time
    months = pd.to_datetime(monthly["mission_month"])
    return monthly[months <= cutoff] if through.is_month_end else monthly[months < cutoff]


def _select(monthly: pd.DataFrame, tiers: list[str], groups: list[str]) -> pd.DataFrame:
    return monthly[monthly["criticality_tier"].isin(tiers) & monthly["mission_group"].isin(groups)]


def proxy_share(
    monthly: pd.DataFrame,
    tiers: list[str],
    groups: list[str] | None = None,
    by_district: bool = False,
) -> pd.DataFrame:
    """Share of missions with response time <= threshold (own approximation), per month."""
    d = _select(monthly, tiers, groups or ["ems"])
    keys = ["mission_month"] + (["district_name"] if by_district else [])
    g = d.groupby(keys, as_index=False)[
        ["mission_count_with_response_time", "mission_count_within_timegoal"]
    ].sum()
    g["share"] = g["mission_count_within_timegoal"] / g["mission_count_with_response_time"]
    return g[g["mission_count_with_response_time"] > 0]


def proxy_by_district(monthly: pd.DataFrame, year: int, tiers: list[str]) -> pd.DataFrame:
    d = _select(monthly, tiers, ["ems"])
    d = d[pd.to_datetime(d["mission_month"]).dt.year == year]
    g = d.groupby("district_name", as_index=False)[
        ["mission_count_with_response_time", "mission_count_within_timegoal"]
    ].sum()
    g["share"] = g["mission_count_within_timegoal"] / g["mission_count_with_response_time"]
    return g[["district_name", "share"]]


def proxy_year(monthly: pd.DataFrame, year: int, tiers: list[str]) -> float:
    d = _select(monthly, tiers, ["ems"])
    d = d[pd.to_datetime(d["mission_month"]).dt.year == year]
    n = d["mission_count_with_response_time"].sum()
    return d["mission_count_within_timegoal"].sum() / n if n else float("nan")
