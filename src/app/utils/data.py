"""Cached loaders for the files in public/app/data/ (the app never touches DuckDB)."""

from __future__ import annotations

import json
import pathlib

import pandas as pd
import streamlit as st

APP_DATA = pathlib.Path(__file__).resolve().parents[3] / "public" / "app" / "data"


@st.cache_data(show_spinner=False)
def load_table(name: str) -> pd.DataFrame:
    return pd.read_parquet(APP_DATA / f"{name}.parquet")


@st.cache_data(show_spinner=False)
def load_geojson(level: str) -> dict:
    return json.loads((APP_DATA / "geo" / f"lor_{level}.geojson").read_text(encoding="utf-8"))


@st.cache_data(show_spinner=False)
def load_meta() -> dict:
    return json.loads((APP_DATA / "meta.json").read_text(encoding="utf-8"))
