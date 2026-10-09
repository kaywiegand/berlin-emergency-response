import pandas as pd
import streamlit as st

from utils import metrics
from utils.common import footer
from utils.data import load_meta, load_table
from utils.plots import counts_by_type_monthly, num, pct, rd_shares_chart, yearly_counts_chart

daily = load_table("missions_daily_citywide")
events = load_table("events")
meta = load_meta()

st.title("Einsatzzahlen")
st.caption("Nach Einsatzart getrennt, wie auf der Open-Data-Seite der Berliner Feuerwehr. Quelle: Tagesreihe der BF (Daily_Data).")

st.subheader("Einsätze pro Monat")
monthly = metrics.complete_months(metrics.monthly_counts(daily), meta["daily_through"], column="month")
st.plotly_chart(counts_by_type_monthly(monthly, events), width="stretch")
st.caption("Markiert sind Sturmlagen laut BF-Darstellung (Spitzen der technischen Hilfeleistung). Der laufende, unvollständige Monat ist ausgeblendet.")

st.subheader("Anstieg über die Jahre")
yearly = metrics.yearly_counts(daily)
full_years = [int(y) for y in yearly["year"]]
c1, c2 = st.columns(2)
start = c1.selectbox("Vergleich von", full_years, index=full_years.index(2019))
end = c2.selectbox("bis", full_years, index=full_years.index(2024))
partial = int(yearly["year"].max()) if yearly["days"].iloc[-1] < 360 else None
st.plotly_chart(yearly_counts_chart(yearly, partial, start, end), width="stretch")
cols = st.columns(3)
for col, (key, name) in zip(cols, [("mission_count_ems", "Rettungsdienst"), ("mission_count_fire", "Brandbekämpfung"), ("mission_count_technical_rescue", "Technische Hilfeleistung")]):
    col.metric(f"{name}: {start} bis {end}", pct(metrics.relative_change(yearly, key, start, end)))
if partial:
    st.caption(f"{partial} ist unvollständig (hell dargestellt).")

st.subheader("Rettungsdiensteinsätze nach Notfallkategorie")
st.markdown("RD1 sind Einsätze der höchsten Dringlichkeit, RD4 der niedrigsten; RD5 sind Abgaben an die Kassenärztliche Vereinigung. "
            "Seit dem **25.03.2025** nutzt die Feuerwehr die Notfallkategorien zur Klassifikation und Beschickung; die Zahlen davor hat sie aus den Dispatchcodes berechnet.")
st.plotly_chart(rd_shares_chart(metrics.rd_year_shares(daily)), width="stretch")
st.caption("RD1 und RD2 (\"kritisch\") machen über die Jahre ungefähr die Hälfte der Einsätze aus. Die Verteilung verschiebt sich ab 2025.")
footer()
