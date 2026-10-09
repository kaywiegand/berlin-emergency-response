import pandas as pd
import streamlit as st

from utils import metrics
from utils.common import deadlines_box, footer
from utils.data import load_geojson, load_meta, load_table
from utils.plots import choropleth, district_comparison, minutes, num, pct, timeline

LEVELS = {"Bezirksregion (143)": "district_area", "Planungsraum (542)": "planning_room", "Prognoseraum (58)": "prediction_area"}

regional = load_table("timegoal_region_yearly")
monthly_all = load_table("missions_monthly")
daily = load_table("missions_daily_citywide")
events = load_table("events")
meta = load_meta()
threshold = meta["timegoal_seconds"]["ems"]
monthly = metrics.complete_months(monthly_all, meta["data_through"])
years = sorted(regional["data_year"].unique())

st.sidebar.header("Filter")
year = st.sidebar.select_slider("Jahr (Karte, Kennzahlen)", options=years, value=years[-1])
level_label = st.sidebar.radio("Kartenebene", list(LEVELS), index=0)
metric_key = st.sidebar.selectbox("Kartenwert", list(metrics.REGION_METRICS), format_func=lambda k: metrics.REGION_METRICS[k][1])
tiers = st.sidebar.multiselect(
    "Dispatch-Stufen (Zeitverlauf Rettungsdienst)", metrics.TIERS, default=metrics.DEFAULT_TIERS,
    help="Stufe des Einsatzes im Notrufsystem. C/D/E kommt der offiziellen Gruppe RD1+RD2 am nächsten (siehe Fristen und Methodik).",
)
districts = st.sidebar.multiselect("Bezirke im Zeitverlauf", sorted(monthly["district_name"].unique()), default=[])
if not tiers:
    st.sidebar.warning("Keine Stufe gewählt, es gilt die Standardauswahl.")
sel = tiers or metrics.DEFAULT_TIERS

st.title("Berliner Rettungsdienst und Feuerwehr: Wie schnell, wo und wann?")
st.caption(
    f"Daten der Berliner Feuerwehr bis {pd.Timestamp(meta['data_through']):%d.%m.%Y}. "
    "Es gelten je Einsatzart unterschiedliche Fristen; Zusammenhänge, keine Ursachen."
)
deadlines_box()

k = metrics.official_kpis(regional, year)
yc = metrics.yearly_counts(daily).set_index("year")
tech_mean = metrics.weighted_monthly(daily[pd.to_datetime(daily["mission_date"]).dt.year == year], "response_time_technical_rescue_mean", "mission_count_technical_rescue")
tech_seconds = float((tech_mean["value"] * 1).mean()) if len(tech_mean) else float("nan")
prev = metrics.official_kpis(regional, year - 1) if year - 1 in years else None

c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("Rettungsdienst")
    st.metric(f"Hilfsfrist-Quote {year} (kritisch)", pct(k["quote"]), help="Anteil kritischer Einsätze, bei denen die Frist von 10 Minuten erreicht wurde (BF Regionaldaten). Soll: 90 %.")
    st.caption(f"Einsätze {year}: {num(k['ems_missions'])} · Ø Zeit kritisch: {minutes(k['mean_response_seconds'])}")
    st.caption("Vorjahreswerte sind nur eingeschränkt vergleichbar: seit 25.03.2025 gelten Notfallkategorien, der Kreis \"kritisch\" ist enger.")
with c2:
    st.subheader("Brandbekämpfung")
    delta = None if prev is None or pd.isna(prev["fire_quote"]) else f"{(k['fire_quote'] - prev['fire_quote']) * 100:+.1f} Pkt".replace(".", ",")
    st.metric(f"Hilfsfrist-Quote {year}", pct(k["fire_quote"]), delta=delta, help="Frist: 14 Funktionen in 15 Minuten; Soll 90 % (Klasse A), 50 % (Klasse B). Hier die Quote der BF-Regionaldaten.")
    st.caption(f"Einsätze {year}: {num(k['fire_missions'])}")
with c3:
    st.subheader("Technische Hilfeleistung")
    st.metric(f"Ø Antwortzeit {year}", minutes(tech_seconds), help="Für technische Hilfeleistung ist keine Frist vereinbart. Mittel der Monatswerte aus der Tagesreihe der BF. Die Seite \"Berliner Feuerwehr in Zahlen\" nennt einen deutlich niedrigeren Durchschnitt (9,92 min); Abgrenzung offen.")
    st.caption(f"Einsätze {year}: {num(yc.loc[year, 'mission_count_technical_rescue']) if year in yc.index else 'n/a'} · keine Frist vereinbart")

column, label, unit, lower_is_better = metrics.REGION_METRICS[metric_key]
st.subheader(f"{label}, {year}")
level = LEVELS[level_label]
rd = regional[regional["region_level"] == level]
values = rd[column].dropna()
st.plotly_chart(
    choropleth(rd[rd["data_year"] == year], load_geojson(level), column, label, unit, lower_is_better, (float(values.min()), float(values.max()))),
    width="stretch",
)
if metric_key == "ems_quote" and year in (min(years), min(years) + 1):
    st.info("Die Quote 2024 ist mit 2025/2026 nicht vergleichbar: Seit dem 25.03.2025 klassifiziert die Feuerwehr Einsätze in Notfallkategorien, der Kreis \"kritischer\" Einsätze ist deutlich enger.")
if metric_key == "technical_median":
    st.caption("Für technische Hilfeleistung gibt es keine Frist; die Karte zeigt nur die Zeit.")

left, right = st.columns([3, 2])
with left:
    st.subheader("Rettungsdienst: Zeitverlauf 2018 bis heute")
    city = metrics.proxy_share(monthly, sel)
    by_district = metrics.proxy_share(monthly, sel, by_district=True)
    by_district = by_district[by_district["district_name"].isin(districts)]
    official_city = pd.DataFrame([{"data_year": y, "share": metrics.official_kpis(regional, y)["quote"]} for y in years])
    st.plotly_chart(timeline(city, by_district, official_city, events, threshold), width="stretch")
with right:
    st.subheader(f"Rettungsdienst: Bezirke im Vergleich, {year}")
    st.plotly_chart(district_comparison(metrics.official_by_district(regional, year), metrics.proxy_share(monthly_all, sel, year=year, by_district=True, by_month=False)[["district_name", "share"]]), width="stretch")

share = metrics.proxy_year(monthly_all, year, sel)
st.caption(f"Eigene Näherung {year} für die gewählten Stufen: {pct(share)} der Rettungsdiensteinsätze innerhalb {threshold} s. Schwelle und Stufen sind Annahmen (Vermutung).")
footer()
