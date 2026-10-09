"""Pure aggregation functions behind the dashboard (no Streamlit, unit-testable)."""

from __future__ import annotations

import pandas as pd

OFFICIAL_LEVEL = "district_area"  # all three Regional_Data levels sum to the same totals
TIERS = ["A", "B", "C", "D", "E", "O", "unknown"]
# C/D/E come closest to the official RD1+RD2 population (overestimate, see 01_exploration_daily); D/E alone is far too narrow.
DEFAULT_TIERS = ["C", "D", "E"]
MISSION_TYPES = {"ems": "Rettungsdienst", "fire": "Brandbekämpfung", "technical": "Technische Hilfeleistung"}

# metric key -> (column, label, unit, lower_is_better)
REGION_METRICS = {
    "ems_quote": ("ems_critical_timegoal_quote", "Rettungsdienst: Hilfsfrist-Quote (kritisch)", "share", False),
    "ems_median": ("response_time_ems_critical_median", "Rettungsdienst: Median Antwortzeit (kritisch)", "seconds", True),
    "fire_quote": ("fire_timegoal_quote", "Brandbekämpfung: Hilfsfrist-Quote", "share", False),
    "fire_pump": ("response_time_fire_time_to_first_pump_median", "Brandbekämpfung: Median bis 1. Löschfahrzeug", "seconds", True),
    "technical_median": ("response_time_technical_rescue_median", "Technische Hilfe: Median Antwortzeit (ohne Frist)", "seconds", True),
}


def official_kpis(regional: pd.DataFrame, year: int) -> dict:
    """City-wide official figures for one year, per mission type."""
    d = regional[(regional["region_level"] == OFFICIAL_LEVEL) & (regional["data_year"] == year)]

    def quote(reached: str, computed: str) -> float:
        n = d[computed].sum()
        return d[reached].sum() / n if n else float("nan")

    def weighted(col: str, weight: str) -> float:
        w = d[weight]
        ok = d[col].notna() & (w > 0)
        return (d.loc[ok, col] * w[ok]).sum() / w[ok].sum() if ok.any() else float("nan")

    return {
        "quote": quote("ems_critical_timegoal_reached", "ems_critical_timegoal_computed"),
        "computed": int(d["ems_critical_timegoal_computed"].sum()),
        "mean_response_seconds": weighted("response_time_ems_critical_mean", "mission_count_ems_critical"),
        "missions": int(d["mission_count_all"].sum()),
        "ems_missions": int(d["mission_count_ems"].sum()),
        "fire_missions": int(d["mission_count_fire"].sum()),
        "fire_quote": quote("fire_timegoal_reached", "fire_timegoal_computed"),
    }


def official_by_district(regional: pd.DataFrame, year: int) -> pd.DataFrame:
    d = regional[(regional["region_level"] == OFFICIAL_LEVEL) & (regional["data_year"] == year)]
    g = d.groupby("district_name", as_index=False)[
        ["ems_critical_timegoal_computed", "ems_critical_timegoal_reached"]
    ].sum()
    g["share"] = g["ems_critical_timegoal_reached"] / g["ems_critical_timegoal_computed"]
    return g[["district_name", "share"]]


def complete_months(df: pd.DataFrame, data_through: str, column: str = "mission_month") -> pd.DataFrame:
    """Drop the last month if the data does not reach its final day."""
    through = pd.Timestamp(data_through)
    cutoff = through.to_period("M").start_time
    months = pd.to_datetime(df[column])
    return df[months <= cutoff] if through.is_month_end else df[months < cutoff]


def proxy_share(
    monthly: pd.DataFrame,
    tiers: list[str],
    year: int | None = None,
    by_district: bool = False,
    by_month: bool = True,
) -> pd.DataFrame:
    """Share of ambulance missions with response time <= threshold (own approximation) for the given dispatch levels.

    Only missions with a time goal count (ambulance service); the denominator is `mission_count_with_timegoal`.
    """
    d = monthly[monthly["criticality_tier"].isin(tiers) & (monthly["mission_group"] == "ems")]
    if year is not None:
        d = d[pd.to_datetime(d["mission_month"]).dt.year == year]
    keys = (["mission_month"] if by_month else []) + (["district_name"] if by_district else [])
    cols = ["mission_count_with_timegoal", "mission_count_within_timegoal"]
    g = d.groupby(keys, as_index=False)[cols].sum() if keys else d[cols].sum().to_frame().T
    g["share"] = g["mission_count_within_timegoal"] / g["mission_count_with_timegoal"]
    return g[g["mission_count_with_timegoal"] > 0]


def proxy_year(monthly: pd.DataFrame, year: int, tiers: list[str]) -> float:
    g = proxy_share(monthly, tiers, year=year, by_month=False)
    return float(g["share"].iloc[0]) if len(g) else float("nan")


# ── daily series (Daily_Data), BF-style charts ────────────────────────────────

def _month(daily: pd.DataFrame) -> pd.Series:
    return pd.to_datetime(daily["mission_date"]).dt.to_period("M").dt.start_time


def monthly_counts(daily: pd.DataFrame) -> pd.DataFrame:
    cols = ["mission_count_ems", "mission_count_fire", "mission_count_technical_rescue"]
    return daily.assign(month=_month(daily)).groupby("month", as_index=False)[cols].sum()


def yearly_counts(daily: pd.DataFrame) -> pd.DataFrame:
    cols = ["mission_count_ems", "mission_count_fire", "mission_count_technical_rescue"]
    g = daily.assign(year=pd.to_datetime(daily["mission_date"]).dt.year).groupby("year", as_index=False)[cols].sum()
    g["days"] = daily.assign(year=pd.to_datetime(daily["mission_date"]).dt.year).groupby("year")["mission_date"].nunique().to_numpy()
    return g


def relative_change(yearly: pd.DataFrame, col: str, start: int, end: int) -> float:
    a = yearly.loc[yearly["year"] == start, col]
    b = yearly.loc[yearly["year"] == end, col]
    return float(b.iloc[0] / a.iloc[0] - 1) if len(a) and len(b) and a.iloc[0] else float("nan")


def weighted_monthly(daily: pd.DataFrame, value_col: str, weight_col: str) -> pd.DataFrame:
    """Monthly mean of a daily statistic, weighted by the daily mission count (seconds)."""
    d = daily[daily[value_col].notna() & (daily[weight_col] > 0)].copy()
    d["w"] = d[weight_col]
    d["wv"] = d[value_col] * d["w"]
    g = d.assign(month=_month(d)).groupby("month", as_index=False)[["wv", "w"]].sum()
    g["value"] = g["wv"] / g["w"]
    return g[["month", "value"]]


def rd_year_shares(daily: pd.DataFrame) -> pd.DataFrame:
    cols = [f"mission_count_rd{i}" for i in range(1, 6)]
    g = daily.assign(year=pd.to_datetime(daily["mission_date"]).dt.year).groupby("year")[cols].sum()
    return g.div(g.sum(axis=1), axis=0).rename(columns=lambda c: c.replace("mission_count_", "").upper())
