import streamlit as st
from src.data.load import load_stats, load_roster
from src.data.clean import filter_active_player_stats, filter_current_season
from src.stats.batting import aggregate_stats
from src.stats.lineup import build_batting_order
from config import CURRENT_SEASON, LOGO_PATH, LAST_SEASON
from utils.formatting import STAT_COLUMN_CONFIG

st.set_page_config(page_title="Bangers Stats", layout="wide")


st.image(LOGO_PATH, width=200)
st.title("Bangers Softball Stats")



# Load
stats_df = load_stats()
roster_df = load_roster()

active_players = filter_active_player_stats(stats_df, roster_df)

this_season = filter_current_season(active_players)

season_summary = aggregate_stats(this_season)
career_summary = aggregate_stats(active_players)

batting_order = build_batting_order(stats_df, roster_df)


# Tabs
tab_batting_order, tab_season_stats, tab_career_stats, tab_player_profile = st.tabs([
    "Batting Order", "Season Stats", "Career Stats", "Player Profile"
])

with tab_batting_order:
    st.subheader("Batting Order")
    st.caption(f"Returning players sorted by {LAST_SEASON} AVG. New players at the bottom.")
    st.dataframe(
        batting_order,
        use_container_width=True,
        hide_index=True,
    )

with tab_season_stats:
    st.subheader("Season Stats")
    st.dataframe(
        season_summary,
        use_container_width=True,
        column_config=STAT_COLUMN_CONFIG,
        hide_index=True)

with tab_career_stats:
    st.subheader("Career Stats")
    st.dataframe(
        career_summary,
        use_container_width=True,
        column_config=STAT_COLUMN_CONFIG,
        hide_index=True)

with tab_player_profile:
    st.write("Coming soon")