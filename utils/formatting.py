# utils/formatting.py
import streamlit as st

STAT_COLUMN_CONFIG = {
    "PlayerName": "Player Name",
    "Games_Played": "Games Played",
    "AVG": st.column_config.NumberColumn(format="%.3f"),
    "OBP": st.column_config.NumberColumn(format="%.3f"),
}