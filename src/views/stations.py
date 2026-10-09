import pandas as pd
import streamlit as st

from utils.common import footer
from utils.data import load_table
from utils.plots import minutes, num, stations_map

stations = load_table("stations")

st.title("Wachen")
st.caption("Standorte der Berufsfeuerwehr (BF), der Freiwilligen Feuerwehr (FF) und Rettungswachen (RW), Stand 2024. Die Ausrückzeit ist die Zeit von der Alarmierung bis zur Übernahme durch die Besatzung, nur dringliche Einsätze, seit 2025.")

st.plotly_chart(stations_map(stations), width="stretch")
st.caption("Punktgröße: RTW-Alarmierungen seit 2025. Wachen ohne Wert haben keine RTW-Alarmierungen in den Ausrückdaten.")

st.subheader("RTW-Ausrückzeit nach Typ")
d = stations[stations["rtw_alarms"] > 0].copy()
d["w"] = d["rtw_alarms"] * d["rtw_turnout_seconds"]
by_type = d.groupby("station_type").agg(stations=("station_id", "count"), alarms=("rtw_alarms", "sum"), w=("w", "sum")).reset_index()
by_type["Ausrückzeit"] = (by_type["w"] / by_type["alarms"]).map(minutes)
st.dataframe(by_type.rename(columns={"station_type": "Typ", "stations": "Wachen", "alarms": "Alarmierungen"}).drop(columns="w"), hide_index=True)
st.caption("Auch Standorte der Freiwilligen Feuerwehr haben RTW-Alarmierungen: Auf FF-Standorten betreibt die BF Rettungswachen.")

st.subheader("Schnellste und langsamste Wachen")
big = d[d["rtw_alarms"] >= 500].sort_values("rtw_turnout_seconds")
cols = ["station_name", "station_type", "district_name", "rtw_alarms", "rtw_turnout_seconds"]
names = {"station_name": "Wache", "station_type": "Typ", "district_name": "Bezirk", "rtw_alarms": "Alarmierungen", "rtw_turnout_seconds": "Ausrückzeit (s)"}
a, b = st.columns(2)
a.markdown("**Schnellste**")
a.dataframe(big.head(8)[cols].rename(columns=names).round({"Ausrückzeit (s)": 0}), hide_index=True)
b.markdown("**Langsamste**")
b.dataframe(big.tail(8)[cols].iloc[::-1].rename(columns=names).round({"Ausrückzeit (s)": 0}), hide_index=True)
st.caption("Nur Wachen mit mindestens 500 RTW-Alarmierungen. Der Bezirk steht so im Standort-Datensatz der BF und weicht bei wenigen Wachen von der Lage ab.")
footer()
