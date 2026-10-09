import streamlit as st

st.set_page_config(page_title="Berlin Emergency Response", layout="wide", initial_sidebar_state="expanded")

pages = [
    st.Page("views/overview.py", title="Übersicht", default=True),
    st.Page("views/counts.py", title="Einsatzzahlen"),
    st.Page("views/arrival_times.py", title="Eintreffzeiten"),
    st.Page("views/stations.py", title="Wachen"),
    st.Page("views/notes.py", title="Fristen und Methodik"),
]
st.navigation(pages).run()
