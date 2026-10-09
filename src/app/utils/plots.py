"""Plotly figures for the dashboard. Pure functions, themed via wgnd."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from wgnd.core.config import cfg
from wgnd.plotly_theme import register, sequential_scale

register()

BERLIN_CENTER = {"lat": 52.51, "lon": 13.40}
SCOPE_COLORS = {
    "weather": cfg.DIM_COLOR,
    "organisation": cfg.PRIMARY_COLOR,
    "timegoal_definition": cfg.COLOR_SIGNAL,
    "call_data": cfg.COLOR_NEGATIVE,
}
TYPE_COLORS = {"ems": cfg.PRIMARY_COLOR, "fire": cfg.COLOR_NEGATIVE, "technical": "#146b30"}


def pct(x: float, digits: int = 1) -> str:
    return "n/a" if pd.isna(x) else f"{x * 100:.{digits}f} %".replace(".", ",")


def num(x: float) -> str:
    return f"{int(x):,}".replace(",", ".")


def minutes(seconds: float) -> str:
    return "n/a" if pd.isna(seconds) else f"{seconds / 60:.1f} min".replace(".", ",")


def add_events(fig: go.Figure, events: pd.DataFrame, scopes: list[str], row: int | None = None, y_top: float = 1.0, step: float = 0.075) -> None:
    """Dashed vertical marker plus label per event of the given scopes."""
    sel = events[events["scope"].isin(scopes)].sort_values("event_start")
    for i, ev in enumerate(sel.itertuples()):
        x = pd.Timestamp(ev.event_start)
        color = SCOPE_COLORS.get(ev.scope, cfg.COLOR_NEUTRAL)
        line = dict(color=color, dash="dash", width=1.3)
        if row is None:
            fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=1, xref="x", yref="paper", line=line)
            fig.add_annotation(x=x, y=y_top - step * (i % 4), xref="x", yref="paper", text=ev.short_label, showarrow=False,
                               xanchor="right", xshift=-4, font=dict(size=11, color=color))
        else:
            fig.add_shape(type="line", x0=x, x1=x, y0=0, y1=1, yref="y domain", line=line, row=row, col=1)
            fig.add_annotation(x=x, y=y_top - step * (i % 3), yref="y domain", text=ev.short_label, showarrow=False,
                               xanchor="left", xshift=4, font=dict(size=11, color=color), row=row, col=1)


# ── overview ──────────────────────────────────────────────────────────────────

def choropleth(df: pd.DataFrame, geojson: dict, value_col: str, label: str, unit: str, lower_is_better: bool,
               value_range: tuple[float, float]) -> go.Figure:
    """One metric per LOR region. `unit` is 'share' or 'seconds'."""
    scale = sequential_scale()
    scale = scale[::-1] if lower_is_better else scale
    fmt = ":.1%" if unit == "share" else ":.0f"
    fig = px.choropleth_map(
        df, geojson=geojson, locations="region_id", featureidkey="properties.region_id", color=value_col,
        range_color=value_range, color_continuous_scale=scale, hover_name="region_name",
        hover_data={"region_id": False, "district_name": True, value_col: fmt},
        labels={value_col: label, "district_name": "Bezirk"},
        map_style="carto-positron", center=BERLIN_CENTER, zoom=9.3, opacity=0.8,
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=520,
        coloraxis_colorbar=dict(title="", tickformat=".0%" if unit == "share" else None),
    )
    return fig


def timeline(city: pd.DataFrame, districts: pd.DataFrame, official: pd.DataFrame, events: pd.DataFrame, threshold_seconds: int) -> go.Figure:
    """Monthly share of ambulance missions within the threshold, official yearly quotes and event markers."""
    fig = go.Figure()
    for name, g in districts.groupby("district_name"):
        fig.add_trace(go.Scatter(x=g["mission_month"], y=g["share"], name=name, mode="lines", line=dict(width=1)))
    fig.add_trace(go.Scatter(x=city["mission_month"], y=city["share"], name="Berlin gesamt (eigene Näherung)", mode="lines",
                             line=dict(width=3, color=cfg.PRIMARY_COLOR)))
    if not official.empty:
        fig.add_trace(go.Scatter(
            x=pd.to_datetime(official["data_year"].astype(str) + "-07-01"), y=official["share"], name="Offizielle Quote (Jahr)",
            mode="markers", marker=dict(size=11, symbol="diamond", color=cfg.COLOR_SIGNAL, line=dict(width=1, color="#222"))))
    add_events(fig, events, ["timegoal_definition", "organisation"])
    fig.update_layout(
        height=460, hovermode="x unified",
        yaxis=dict(tickformat=".0%", title=f"Anteil Einsätze ≤ {threshold_seconds} s"),
        xaxis=dict(range=[city["mission_month"].min(), city["mission_month"].max()]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig


def district_comparison(official: pd.DataFrame, proxy: pd.DataFrame) -> go.Figure:
    d = official.merge(proxy, on="district_name", suffixes=("_official", "_proxy")).sort_values("share_official")
    fig = go.Figure()
    fig.add_bar(y=d["district_name"], x=d["share_official"], name="Offiziell (Hilfsfrist-Quote)", orientation="h", marker_color=cfg.COLOR_SIGNAL)
    fig.add_bar(y=d["district_name"], x=d["share_proxy"], name="Eigene Näherung", orientation="h", marker_color=cfg.PRIMARY_COLOR)
    fig.update_layout(barmode="group", height=460, xaxis=dict(tickformat=".0%", range=[0, 1]),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(l=10, r=10, t=30, b=10))
    return fig


# ── BF-style charts ───────────────────────────────────────────────────────────

def counts_by_type_monthly(monthly: pd.DataFrame, events: pd.DataFrame) -> go.Figure:
    """Missions per month, one panel per mission type (as on the BF open data page), storms marked."""
    panels = [("mission_count_ems", "Rettungsdienst", "ems"), ("mission_count_fire", "Brandbekämpfung", "fire"),
              ("mission_count_technical_rescue", "Technische Hilfeleistung", "technical")]
    fig = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.07, subplot_titles=[p[1] for p in panels])
    for r, (col, _, key) in enumerate(panels, start=1):
        fig.add_trace(go.Scatter(x=monthly["month"], y=monthly[col], mode="lines", fill="tozeroy", line=dict(color=TYPE_COLORS[key], width=2),
                                 showlegend=False, hovertemplate="%{x|%b %Y}: %{y:,.0f}<extra></extra>"), row=r, col=1)
    add_events(fig, events, ["weather"], row=3)
    fig.update_yaxes(rangemode="tozero", tickformat=",")
    fig.update_layout(height=640, margin=dict(l=10, r=10, t=40, b=10))
    return fig


def yearly_counts_chart(yearly: pd.DataFrame, partial_year: int | None, start: int, end: int) -> go.Figure:
    """Missions per year and type, the comparison years highlighted, the running year drawn lighter."""
    panels = [("mission_count_ems", "Rettungsdienst", "ems"), ("mission_count_fire", "Brandbekämpfung", "fire"),
              ("mission_count_technical_rescue", "Technische Hilfeleistung", "technical")]
    fig = make_subplots(rows=1, cols=3, subplot_titles=[p[1] for p in panels])
    for c, (col, _, key) in enumerate(panels, start=1):
        colors = []
        for y in yearly["year"]:
            if y == partial_year:
                colors.append("rgba(150,150,150,0.45)")
            elif y in (start, end):
                colors.append(TYPE_COLORS[key])
            else:
                colors.append("rgba(150,150,150,0.8)")
        fig.add_trace(go.Bar(x=yearly["year"].astype(str), y=yearly[col], marker_color=colors, showlegend=False,
                             hovertemplate="%{x}: %{y:,.0f}<extra></extra>"), row=1, col=c)
    fig.update_yaxes(tickformat=",", rangemode="tozero")
    fig.update_layout(height=420, margin=dict(l=10, r=10, t=40, b=10))
    return fig


def response_chart(monthly: pd.DataFrame, events: pd.DataFrame, title: str, band: pd.DataFrame | None = None,
                   reference_minutes: float | None = None, reference_label: str = "") -> go.Figure:
    """Monthly mean response time in minutes, optional ±0.5 standard deviation band and reference line (the time goal)."""
    fig = go.Figure()
    if band is not None:
        fig.add_trace(go.Scatter(x=band["month"], y=band["upper"] / 60, mode="lines", line=dict(width=0), showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=band["month"], y=band["lower"] / 60, mode="lines", line=dict(width=0), fill="tonexty",
                                 fillcolor="rgba(150,150,150,0.2)", name="Mittelwert ± 0,5 Standardabweichung", hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=monthly["month"], y=monthly["value"] / 60, mode="lines", name="Mittlere Zeit",
                             line=dict(width=2.5, color=cfg.PRIMARY_COLOR), hovertemplate="%{x|%b %Y}: %{y:.1f} min<extra></extra>"))
    if reference_minutes:
        fig.add_hline(y=reference_minutes, line=dict(color=cfg.COLOR_SIGNAL, dash="dot"), annotation_text=reference_label,
                      annotation_position="top left")
    add_events(fig, events, ["timegoal_definition", "organisation"])
    fig.update_layout(height=430, title=title, yaxis=dict(title="Minuten"), hovermode="x unified",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(l=10, r=10, t=60, b=10))
    return fig


def fire_chart(series: dict[str, pd.DataFrame], events: pd.DataFrame, reference_minutes: float) -> go.Figure:
    colors = [cfg.COLOR_SIGNAL, cfg.PRIMARY_COLOR, cfg.COLOR_NEGATIVE]
    fig = go.Figure()
    for (name, df), color in zip(series.items(), colors):
        fig.add_trace(go.Scatter(x=df["month"], y=df["value"] / 60, mode="lines", name=name, line=dict(width=2, color=color),
                                 hovertemplate="%{x|%b %Y}: %{y:.1f} min<extra></extra>"))
    fig.add_hline(y=reference_minutes, line=dict(color=cfg.DIM_COLOR, dash="dot"), annotation_text="Frist 15 min (14 Funktionen)", annotation_position="top left")
    add_events(fig, events, ["timegoal_definition"])
    fig.update_layout(height=430, yaxis=dict(title="Minuten"), hovermode="x unified",
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(l=10, r=10, t=30, b=10))
    return fig


def rd_shares_chart(shares: pd.DataFrame) -> go.Figure:
    labels = {"RD1": "RD1 Reanimation, Erstickungsanfall", "RD2": "RD2 Herzinfarkt, Bewusstseinsstörung, starke Blutung",
              "RD3": "RD3 Sturz, Ohnmacht, psychiatrische Notfälle", "RD4": "RD4 Bauchschmerzen, Erkrankungen mit Risikofaktoren",
              "RD5": "RD5 Abgabe an die Kassenärztliche Vereinigung"}
    fig = go.Figure()
    for col in shares.columns:
        fig.add_bar(x=shares.index.astype(str), y=shares[col], name=labels.get(col, col))
    fig.update_layout(barmode="stack", height=430, yaxis=dict(tickformat=".0%", title="Anteil der Rettungsdiensteinsätze"),
                      legend=dict(orientation="h", yanchor="top", y=-0.12, x=0), margin=dict(l=10, r=10, t=30, b=10))
    return fig


def stations_map(df: pd.DataFrame) -> go.Figure:
    d = df.copy()
    d["size"] = d["rtw_alarms"].clip(lower=0).pow(0.5).clip(lower=3)
    d["turnout"] = d["rtw_turnout_seconds"].round(0)
    fig = px.scatter_map(
        d, lat="lat", lon="lon", color="station_type", size="size", size_max=18, hover_name="station_name",
        hover_data={"station_type": True, "district_name": True, "rtw_alarms": ":,", "turnout": True, "lat": False, "lon": False, "size": False},
        labels={"station_type": "Typ", "district_name": "Bezirk", "rtw_alarms": "RTW-Alarmierungen seit 2025", "turnout": "Ausrückzeit RTW (s)"},
        color_discrete_map={"BF": cfg.PRIMARY_COLOR, "FF": cfg.COLOR_SIGNAL, "RW": cfg.COLOR_NEGATIVE},
        map_style="carto-positron", center=BERLIN_CENTER, zoom=9.3,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0), height=560, legend=dict(orientation="h", yanchor="bottom", y=0.01, x=0.01))
    return fig
