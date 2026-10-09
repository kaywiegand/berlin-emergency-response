import json

import streamlit as st

from utils.common import footer
from utils.data import APP_DATA

STRENGTH = {"belegt": "Belegt", "hinweis": "Hinweis (Zusammenhang, keine Ursache)", "offen": "Offen"}
GROUPS = {"all": "Alle Einsatzarten", "ems": "Rettungsdienst", "fire": "Brandbekämpfung", "technical": "Technische Hilfeleistung"}

st.title("Befunde")
st.caption("Aussagen aus dem Notebook `04_insights`, nach Einsatzart getrennt. Jeder Befund nennt seine Stärke und den Beleg.")

data = json.loads((APP_DATA / "insights.json").read_text(encoding="utf-8"))
strengths = st.multiselect("Stärke", list(STRENGTH), default=list(STRENGTH), format_func=STRENGTH.get)

for key, label in GROUPS.items():
    items = [i for i in data["insights"] if i["mission_type"] == key and i["strength"] in strengths]
    if not items:
        continue
    st.subheader(label)
    for item in items:
        with st.container(border=True):
            st.markdown(f"**{item['title']}**")
            st.write(item["text"])
            st.caption(f"{STRENGTH[item['strength']]} · Beleg: " + "; ".join(item["evidence"]))
            if item["caveat"]:
                st.caption(f"Einschränkung: {item['caveat']}")
footer()
