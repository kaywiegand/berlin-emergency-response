import streamlit as st

from utils.common import DEADLINES_MD, footer
from utils.data import load_meta, load_table

events = load_table("events")
meta = load_meta()

st.title("Fristen und Methodik")

st.subheader("Fristen je Einsatzart")
st.markdown(DEADLINES_MD)

st.subheader("Was \"kritisch\" bedeutet")
st.markdown(
    "- **Offiziell** (Regionaldaten der BF): Quote der kritischen Rettungsdiensteinsätze, bei denen die Hilfsfrist erreicht wurde (`erreicht / berechnet`).\n"
    "- **Notfallkategorien:** Seit dem 25.03.2025 klassifiziert die Feuerwehr Rettungsdiensteinsätze in RD1 bis RD5; RD1 und RD2 sind \"kritisch\". "
    "Davor war die Gruppe \"kritisch\" mit rund 96 % aller Rettungsdiensteinsätze deutlich weiter gefasst, danach rund 55 bis 60 %. Die Quote steigt dadurch scheinbar.\n"
    "- **Vergleichbare Gruppe:** RD1 plus RD2 macht in der Tagesreihe der BF über den Stichtag hinweg ungefähr die Hälfte der Rettungsdiensteinsätze aus.\n"
    f"- **Eigene Näherung** (Zeitverlauf je Bezirk): Anteil der Rettungsdiensteinsätze der Dispatch-Stufen C, D und E mit Antwortzeit unter {meta['timegoal_seconds']['ems']} s. "
    "Die Stufen sind aus dem Notrufsystem; sie bilden die Kategorien nur ungefähr ab (sie überschätzen RD1+RD2 je nach Jahr um rund ein Zehntel bis ein Viertel). Schwelle und Stufen sind Annahmen."
)

st.subheader("Strukturänderungen und Ereignisse")
view = events[["event_start", "short_label", "title", "source", "source_verified"]].rename(
    columns={"event_start": "Datum", "short_label": "Ereignis", "title": "Beschreibung", "source": "Quelle", "source_verified": "Beleg geprüft"}
)
st.dataframe(view, hide_index=True)

st.subheader("Grenzen der Daten")
st.markdown(
    "- Keine Uhrzeit und keine Einsatzkoordinaten, nur der Bezirk (12). Regionaldaten nur als Jahresaggregat ab 2024.\n"
    "- Bei einem Teil der Einsätze fehlt die Antwortzeit, bei hohen Dispatch-Stufen häufiger.\n"
    "- Wachen-Standorte haben den Stand 2024; seitdem neue Wachen fehlen.\n"
    "- Gezeigt werden Zusammenhänge, keine Ursachen."
)
footer()
