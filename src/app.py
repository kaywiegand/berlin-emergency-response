import pandas as pd
import streamlit as st

from utils import metrics
from utils.data import load_geojson, load_meta, load_table
from utils.plots import choropleth, district_comparison, num, pct, timeline

THRESHOLD_SECONDS = 600  # keep in sync with dbt var timegoal_seconds
LEVELS = {"Bezirksregion (143)": "district_area", "Planungsraum (542)": "planning_room", "Prognoseraum (58)": "prediction_area"}

st.set_page_config(page_title="Berlin Emergency Response", layout="wide", initial_sidebar_state="expanded")

regional = load_table("timegoal_region_yearly")
monthly_all = load_table("missions_monthly")
events = load_table("events")
meta = load_meta()
monthly = metrics.complete_months(monthly_all, meta["data_through"])

years = sorted(regional["data_year"].unique())

st.sidebar.header("Filter")
year = st.sidebar.select_slider("Jahr (Karte, Kennzahlen)", options=years, value=years[-1])
level_label = st.sidebar.radio("Kartenebene", list(LEVELS), index=0)
tiers = st.sidebar.multiselect(
    "Kritikalitätsstufen (Zeitverlauf)", metrics.TIERS, default=metrics.DEFAULT_TIERS,
    help="Dispatch-Stufe des Einsatzes. D/E dient als Näherung für 'kritisch'.",
)
districts = st.sidebar.multiselect("Bezirke im Zeitverlauf", sorted(monthly["district_name"].unique()), default=[])

st.title("Berliner Rettungsdienst: Wird die Hilfsfrist gehalten?")
st.caption(
    f"Daten der Berliner Feuerwehr bis {pd.Timestamp(meta['data_through']):%d.%m.%Y}. "
    "Beschreibt Struktur, keine Bewertung von Einsatzkräften."
)

k = metrics.official_kpis(regional, year)
prev = metrics.official_kpis(regional, year - 1) if year - 1 in years else None
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    f"Hilfsfrist-Quote {year} (offiziell)", pct(k["quote"]),
    delta=None if prev is None else f"{(k['quote'] - prev['quote']) * 100:+.1f} Pkt".replace(".", ","),
    help="Anteil kritischer Rettungsdiensteinsätze innerhalb der Hilfsfrist, laut BF Regional_Data. "
         "Die Grundgesamtheit 'kritisch' ändert sich 2024→2025, der Vorjahresvergleich ist nur eingeschränkt aussagekräftig.",
)
c2.metric("Ø Antwortzeit kritisch", f"{k['mean_response_seconds']:.0f} s")
c3.metric("Einsätze gesamt", num(k["missions"]))
share = metrics.proxy_year(monthly_all, year, tiers or metrics.DEFAULT_TIERS)
c4.metric(
    f"Anteil ≤ {THRESHOLD_SECONDS} s (Näherung)", pct(share),
    help=f"Eigene Berechnung: Rettungsdiensteinsätze der gewählten Stufen mit Antwortzeit ≤ {THRESHOLD_SECONDS} s.",
)

st.subheader(f"Hilfsfrist-Quote nach Region, {year}")
level = LEVELS[level_label]
rd = regional[(regional["region_level"] == level)]
value_range = (float(rd["ems_critical_timegoal_quote"].min()), float(rd["ems_critical_timegoal_quote"].max()))
st.plotly_chart(
    choropleth(rd[rd["data_year"] == year], load_geojson(level), value_range),
    use_container_width=True,
)
if year == min(years) or year == min(years) + 1:
    st.info("Die Quote 2024 ist mit 2025/2026 nicht vergleichbar: die Grundgesamtheit 'kritischer' Einsätze wurde ab 2025 enger gefasst.")

left, right = st.columns([3, 2])
with left:
    st.subheader("Zeitverlauf 2018 bis heute")
    sel = tiers or metrics.DEFAULT_TIERS
    city = metrics.proxy_share(monthly, sel)
    by_district = metrics.proxy_share(monthly, sel, by_district=True)
    by_district = by_district[by_district["district_name"].isin(districts)]
    official_city = pd.DataFrame(
        [{"data_year": y, "share": metrics.official_kpis(regional, y)["quote"]} for y in years]
    )
    st.plotly_chart(
        timeline(city, by_district, official_city, events, THRESHOLD_SECONDS), use_container_width=True
    )
with right:
    st.subheader(f"Bezirke im Vergleich, {year}")
    st.plotly_chart(
        district_comparison(metrics.official_by_district(regional, year), metrics.proxy_by_district(monthly_all, year, sel)),
        use_container_width=True,
    )

with st.expander("Methodik und Grenzen"):
    st.markdown(
        f"""
- **Offizielle Quote:** `mission_count_ems_critical_timegoal_reached / _computed` aus den Regionaldaten der BF, nur 2024 bis heute veröffentlicht.
- **Eigene Näherung:** Anteil der Rettungsdiensteinsätze der gewählten Dispatch-Stufen mit Antwortzeit ≤ {THRESHOLD_SECONDS} s.
  Schwelle und Stufen-Zuordnung sind Annahmen (Vermutung); sie reproduzieren die offizielle Quote nicht in allen Jahren.
- **Definitionsbruch:** Die Zahl 'kritischer' Einsätze sinkt von 2024 auf 2025 deutlich. Die Quote steigt dadurch scheinbar, ohne dass der Rettungsdienst schneller wurde.
- **Letzter Monat:** unvollständige Monate werden im Zeitverlauf nicht dargestellt.
        """
    )

st.markdown("---")
st.caption(
    "Einsatzdaten: Berliner Feuerwehr, BF-Open-Data, CC BY 4.0. "
    "Flächen: Amt für Statistik Berlin-Brandenburg / Statistische Einheiten im INSPIRE-Datenmodell "
    "(Lebensweltlich Orientierte Räume 01.01.2021), CC BY 3.0 DE."
)
