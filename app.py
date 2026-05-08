import pandas as pd
import streamlit as st
from src.data.load import load_stats, load_roster
from src.data.clean import filter_active_player_stats, filter_current_season
from src.stats.batting import aggregate_stats, season_by_season_stats
from src.stats.lineup import build_batting_order
from config import CURRENT_SEASON, LOGO_PATH, LAST_SEASON, SEASON_ORDER
from utils.formatting import STAT_COLUMN_CONFIG, player_photo_path

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

season_by_season = season_by_season_stats(active_players)

# Add ranks (1 = best, descending for higher-is-better)
career_summary["AVG_Rank"] = career_summary["AVG"].rank(ascending=False, method="min").astype(int)
career_summary["OBP_Rank"] = career_summary["OBP"].rank(ascending=False, method="min").astype(int)
career_summary["H_Rank"] = career_summary["H"].rank(ascending=False, method="min").astype(int)
career_summary["GP_Rank"] = career_summary["Games_Played"].rank(ascending=False, method="min").astype(int)


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
    st.subheader("Player Profile")

    player = st.selectbox(
        "Select a player",
        sorted(season_by_season["PlayerName"].unique())
    )

    # Pull the selected player's career row
    p = career_summary[career_summary["PlayerName"] == player].iloc[0]
    total_players = len(career_summary)

    # Photo + name + KPIs side-by-side
    photo_col, info_col = st.columns([1, 4], vertical_alignment="center")

    with photo_col:
        st.image(player_photo_path(player), width=140)

    with info_col:
        st.markdown(f"### {player}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Games Played", int(p["Games_Played"]), f"#{p['GP_Rank']} of {total_players}", delta_color="off")
        k2.metric("AVG", f"{p['AVG']:.3f}", f"#{p['AVG_Rank']} of {total_players}", delta_color="off")
        k3.metric("OBP", f"{p['OBP']:.3f}", f"#{p['OBP_Rank']} of {total_players}", delta_color="off")
        k4.metric("Hits", int(p["H"]), f"#{p['H_Rank']} of {total_players}", delta_color="off")

    player_history = season_by_season[season_by_season["PlayerName"] == player].copy()
    player_history["Season"] = pd.Categorical(
        player_history["Season"],
        categories=SEASON_ORDER,
        ordered=True,
    )

    player_history = player_history.sort_values("Season")
    player_history.drop("PlayerName",axis=1, inplace=True)

    st.line_chart(player_history, x="Season", y="AVG")
    
    st.dataframe(
        player_history,
        use_container_width=True,
        hide_index=True,
        column_config={
            "PlayerName": "Player Name",
            "Games_Played": "Games Played",
            "AVG": st.column_config.NumberColumn(format="%.3f"),
            "OBP": st.column_config.NumberColumn(format="%.3f"),
        },
    )