"""Shared Streamlit building blocks: deadlines box, footer."""

from __future__ import annotations

import streamlit as st

DEADLINES_MD = """
| Einsatzart | Vorgabe | Gemessen als |
|---|---|---|
| **Rettungsdienst** | Erstes Rettungsmittel innerhalb von 10 Minuten, Erreichungsgrad 90 % (Schutzziel, Planungsgröße) | Zeit bis zum Eintreffen des ersten Fahrzeugs |
| **Brandbekämpfung** | 14 Funktionen innerhalb von 15 Minuten; Erreichungsgrad 90 % (Klasse A), 50 % (Klasse B) | Zeit bis zum 1. Löschfahrzeug, zur 1. Drehleiter, bis 14 Einsatzkräfte vor Ort sind |
| **Technische Hilfeleistung** | keine Frist und kein Erreichungsgrad vereinbart | nur die durchschnittlich erreichte Zeit wird ausgewiesen |

Quelle: [Berliner Feuerwehr in Zahlen](https://www.berliner-feuerwehr.de/ueber-uns/berliner-feuerwehr-in-zahlen-2024-1/).
Die Hilfsfrist läuft vom Beginn der Notrufabfrage bis zum Eintreffen der ersten Einsatzkräfte.
"""


def deadlines_box(expanded: bool = False) -> None:
    with st.expander("Fristen je Einsatzart", expanded=expanded):
        st.markdown(DEADLINES_MD)


def footer() -> None:
    st.markdown("---")
    st.caption(
        "Einsatzdaten: Berliner Feuerwehr, BF-Open-Data, CC BY 4.0. Wachen-Standorte: Berliner Feuerwehr, Geoportal Berlin, dl-de-zero-2.0. "
        "Flächen: Amt für Statistik Berlin-Brandenburg / Statistische Einheiten im INSPIRE-Datenmodell "
        "(Lebensweltlich Orientierte Räume 01.01.2021), CC BY 3.0 DE. Zusammenhänge, keine Ursachen; keine Bewertung von Einsatzkräften."
    )
