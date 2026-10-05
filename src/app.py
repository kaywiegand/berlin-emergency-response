import streamlit as st
import duckdb
import pandas as pd
from datetime import datetime

# Importiere unsere Plot-Funktionen aus dem utils-Ordner
from utils.plots import (
    plot_mission_trend,
    plot_mission_breakdown,
    plot_weekday_distribution,
    plot_response_time
)

# 1. Streamlit Seitenkonfiguration
st.set_page_config(
    page_title="Berlin Emergency Dashboard",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Daten laden mit Caching (liest direkt aus der DuckDB)
@st.cache_resource
def load_data():
    # Pfad zur DuckDB (wird vom Root-Verzeichnis aus aufgerufen)
    db_path = "data/berlin_emergency.duckdb"
    con = duckdb.connect(db_path, read_only=True)
    df = con.sql("SELECT * FROM fct_missions_daily ORDER BY mission_date ASC").df()
    con.close()
    
    # Sicherstellen, dass mission_date ein datetime.date Objekt ist
    df['mission_date'] = pd.to_datetime(df['mission_date']).dt.date
    return df

df = load_data()

# 3. Sidebar Filter
st.sidebar.header("Filter & Zeitraum")
min_date = df['mission_date'].min()
max_date = df['mission_date'].max()

date_range = st.sidebar.date_input(
    "Datumsbereich wählen",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Filter anwenden
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['mission_date'] >= start_date) & (df['mission_date'] <= end_date)]
else:
    filtered_df = df

# 4. Dashboard Header
st.title("🚨 Berliner Notfalleinsätze – Live Analytics")
st.markdown("Automated ELT Pipeline Dashboard powered by **DuckDB**, **dbt**, **Plotly** & **Streamlit**.")
st.markdown("---")

if filtered_df.empty:
    st.warning("Für den gewählten Zeitraum sind keine Daten vorhanden.")
else:
    # 5. KPI-Metriken (Top-Row)
    total_missions_sum = int(filtered_df['total_missions'].sum())
    avg_daily_missions = int(filtered_df['total_missions'].mean())
    avg_response_time = round(filtered_df['median_response_time_seconds'].mean(), 1)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Gesamteinsätze im Zeitraum", value=f"{total_missions_sum:,}".replace(",", "."))
    with col2:
        st.metric(label="Ø Einsätze pro Tag", value=f"{avg_daily_missions:,}".replace(",", "."))
    with col3:
        st.metric(label="Ø Median-Antwortzeit", value=f"{avg_response_time} sek")

    st.markdown("---")

    # 6. Layout der Charts (2 Spalten Layout)
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.plotly_chart(plot_mission_trend(filtered_df), use_container_width=True)
        
    with row1_col2:
        st.plotly_chart(plot_mission_breakdown(filtered_df), use_container_width=True)

    row2_col1, row2_col2 = st.columns(2)
    
    with row2_col1:
        st.plotly_chart(plot_weekday_distribution(filtered_df), use_container_width=True)
        
    with row2_col2:
        st.plotly_chart(plot_response_time(filtered_df), use_container_width=True)

# 7. Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Berlin Emergency Response Pipeline • Portfolio Project</p>", unsafe_allow_html=True)