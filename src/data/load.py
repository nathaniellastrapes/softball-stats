import pandas as pd
import streamlit as st
from config import STAT_SHEET_URL, DATA_RAW, ACTIVE_ROSTER, SEASON_ORDER

@st.cache_data(ttl=300)  # refresh every 5 minutes
def load_stats():
    try:
        df = pd.read_csv(STAT_SHEET_URL)
    except Exception as e:
        st.warning(f"Could not load from Google Sheets, using local backup. ({e})")
        df = pd.read_csv(DATA_RAW)

    df["Season"] = pd.Categorical(df["Season"], categories=SEASON_ORDER, ordered=True)
    return df

@st.cache_data
def load_roster():
    return pd.read_csv(ACTIVE_ROSTER)