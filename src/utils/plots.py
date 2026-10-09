"""Plotly figures for the dashboard. Pure functions, themed via wgnd."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wgnd.core.config import cfg
from wgnd.plotly_theme import register, sequential_scale

register()

BERLIN_CENTER = {"lat": 52.51, "lon": 13.40}
EVENT_COLORS = {"call_data": cfg.COLOR_NEUTRAL, "timegoal_definition": cfg.COLOR_SIGNAL}


def pct(x: float, digits: int = 1) -> str:
    return "n/a" if pd.isna(x) else f"{x * 100:.{digits}f} %".replace(".", ",")


def num(x: float) -> str:
    return f"{int(x):,}".replace(",", ".")


def choropleth(df: pd.DataFrame, geojson: dict, value_range: tuple[float, float]) -> go.Figure:
    """Official Hilfsfrist quote per LOR region."""
    fig = px.choropleth_map(
        df,
        geojson=geojson,
        locations="region_id",
        featureidkey="properties.region_id",
        color="ems_critical_timegoal_quote",
        range_color=value_range,
        color_continuous_scale=sequential_scale(),
        hover_name="region_name",
        hover_data={
            "region_id": False,
            "district_name": True,
            "ems_critical_timegoal_quote": ":.1%",
            "ems_critical_timegoal_computed": ":,",
        },
        labels={
            "ems_critical_timegoal_quote": "Hilfsfrist-Quote",
            "district_name": "Bezirk",
            "ems_critical_timegoal_computed": "Einsätze (berechnet)",
        },
        map_style="carto-positron",
        center=BERLIN_CENTER,
        zoom=9.3,
        opacity=0.8,
    )
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=520,
        coloraxis_colorbar=dict(title="Quote", tickformat=".0%"),
    )
    return fig


def timeline(
    city: pd.DataFrame,
    districts: pd.DataFrame,
    official: pd.DataFrame,
    events: pd.DataFrame,
    threshold_seconds: int,
) -> go.Figure:
    """Monthly share of missions within the threshold, official yearly quotes and event markers."""
    fig = go.Figure()
    for name, g in districts.groupby("district_name"):
        fig.add_trace(
            go.Scatter(x=g["mission_month"], y=g["share"], name=name, mode="lines", line=dict(width=1))
        )
    fig.add_trace(
        go.Scatter(
            x=city["mission_month"],
            y=city["share"],
            name="Berlin gesamt (eigene Näherung)",
            mode="lines",
            line=dict(width=3, color=cfg.PRIMARY_COLOR),
        )
    )
    if not official.empty:
        fig.add_trace(
            go.Scatter(
                x=pd.to_datetime(official["data_year"].astype(str) + "-07-01"),
                y=official["share"],
                name="Offizielle Quote (Jahr)",
                mode="markers",
                marker=dict(size=11, symbol="diamond", color=cfg.COLOR_SIGNAL, line=dict(width=1, color="#222")),
            )
        )
    for i, ev in enumerate(events.itertuples()):
        color = EVENT_COLORS.get(ev.scope, cfg.COLOR_NEUTRAL)
        fig.add_vline(x=pd.Timestamp(ev.event_start).timestamp() * 1000, line=dict(color=color, dash="dash", width=1.5))
        fig.add_annotation(
            x=pd.Timestamp(ev.event_start), y=1 - 0.08 * i, yref="paper", text=ev.short_label,
            showarrow=False, xanchor="right", xshift=-4, font=dict(size=11, color=color),
        )
    fig.update_layout(
        height=460,
        hovermode="x unified",
        yaxis=dict(tickformat=".0%", title=f"Anteil Einsätze ≤ {threshold_seconds} s"),
        xaxis=dict(range=[city["mission_month"].min(), city["mission_month"].max()]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0),
        margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig


def district_comparison(official: pd.DataFrame, proxy: pd.DataFrame) -> go.Figure:
    d = official.merge(proxy, on="district_name", suffixes=("_official", "_proxy")).sort_values("share_official")
    fig = go.Figure()
    fig.add_bar(y=d["district_name"], x=d["share_official"], name="Offiziell (Hilfsfrist-Quote)", orientation="h",
                marker_color=cfg.COLOR_SIGNAL)
    fig.add_bar(y=d["district_name"], x=d["share_proxy"], name="Eigene Näherung", orientation="h",
                marker_color=cfg.PRIMARY_COLOR)
    fig.update_layout(
        barmode="group", height=460, xaxis=dict(tickformat=".0%", range=[0, 1]),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), margin=dict(l=10, r=10, t=30, b=10),
    )
    return fig
