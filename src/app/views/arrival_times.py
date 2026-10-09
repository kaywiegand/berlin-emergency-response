import pandas as pd
import streamlit as st

from utils import metrics
from utils.common import footer
from utils.data import load_meta, load_table
from utils.plots import fire_chart, minutes, response_chart

daily = load_table("missions_daily_citywide")
events = load_table("events")
meta = load_meta()


def monthly_complete(df: pd.DataFrame) -> pd.DataFrame:
    return metrics.complete_months(df, meta["daily_through"], column="month")


st.title("Eintreffzeiten")
st.caption("Mittelwerte der Monate, aus den Tageswerten der BF gewichtet mit der Einsatzzahl. Die BF rechnet zwei Minuten für Notruf und Disposition hinzu; die Werte entsprechen den Diagrammen der Open-Data-Seite.")

tab_ems, tab_cpr, tab_fire, tab_tech = st.tabs(["Rettungsdienst", "Reanimation", "Brandbekämpfung", "Technische Hilfe"])

with tab_ems:
    st.markdown("**Frist:** erstes Rettungsmittel innerhalb von 10 Minuten, Soll-Erreichungsgrad 90 %. Gezeigt sind die kritischen Rettungsdiensteinsätze.")
    mean = monthly_complete(metrics.weighted_monthly(daily, "response_time_ems_critical_mean", "mission_count_ems_critical"))
    std = monthly_complete(metrics.weighted_monthly(daily, "response_time_ems_critical_std", "mission_count_ems_critical"))
    band = mean.merge(std, on="month", suffixes=("", "_std")).assign(upper=lambda d: d["value"] + 0.5 * d["value_std"], lower=lambda d: d["value"] - 0.5 * d["value_std"])
    st.plotly_chart(response_chart(mean, events, "Mittlere Hilfsfrist, kritische Rettungsdiensteinsätze", band=band, reference_minutes=10, reference_label="Frist 10 min"), width="stretch")
    st.caption("Zwei Strukturänderungen laut BF-Darstellung verschieben die Kurve: die Einführung des RTW-B (Basic Life Support) ab Januar 2023 und die Notfallkategorien seit dem 25.03.2025. Sprünge an diesen Stellen sind keine Leistungsänderung allein.")

with tab_cpr:
    st.markdown("**Frist:** wie Rettungsdienst (10 Minuten). Gezeigt sind kritische Einsätze, bei denen im Notrufgespräch eine Reanimation erkannt wurde.")
    cpr = monthly_complete(metrics.weighted_monthly(daily, "response_time_ems_critical_cpr_mean", "mission_count_ems_critical_cpr"))
    st.plotly_chart(response_chart(cpr, events, "Mittlere Hilfsfrist, Reanimationen", reference_minutes=10, reference_label="Frist 10 min"), width="stretch")

with tab_fire:
    st.markdown("**Frist:** 14 Funktionen innerhalb von 15 Minuten (Erreichungsgrad 90 % Klasse A, 50 % Klasse B). Gemessen werden drei Zeiten: bis zum ersten Löschfahrzeug, zur ersten Drehleiter und bis 14 Einsatzkräfte vor Ort sind.")
    series = {
        "bis 14 Einsatzkräfte": monthly_complete(metrics.weighted_monthly(daily, "response_time_fire_time_to_full_crew_mean", "mission_count_fire")),
        "bis 1. Drehleiter": monthly_complete(metrics.weighted_monthly(daily, "response_time_fire_time_to_first_ladder_mean", "mission_count_fire")),
        "bis 1. Löschfahrzeug": monthly_complete(metrics.weighted_monthly(daily, "response_time_fire_time_to_first_pump_mean", "mission_count_fire")),
    }
    st.plotly_chart(fire_chart(series, events, 15), width="stretch")

with tab_tech:
    st.markdown("**Frist:** keine Frist und kein Erreichungsgrad vereinbart; die BF weist nur die durchschnittlich erreichte Zeit aus.")
    tech = monthly_complete(metrics.weighted_monthly(daily, "response_time_technical_rescue_mean", "mission_count_technical_rescue"))
    st.plotly_chart(response_chart(tech, events.iloc[0:0], "Mittlere Antwortzeit, technische Hilfeleistung"), width="stretch")
    st.caption(f"Letzter Monatswert: {minutes(float(tech['value'].iloc[-1]))}.")
footer()
