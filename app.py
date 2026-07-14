import pandas as pd
import streamlit as st
from src.data.load import (
    load_season_stats, load_career_stats, get_current_season,
    get_last_season, get_season_order, load_current_roster,
    load_alltime_record, load_season_record, load_team_record_by_opponent,
    load_player_vs_opponent
)
from config import LOGO_PATH
from utils.formatting import STAT_COLUMN_CONFIG, player_photo_path

st.set_page_config(page_title="Bangers Stats", layout="wide")

st.image(LOGO_PATH, width=200)

if st.button("🔄 Refresh data"):
    st.cache_data.clear()
    st.rerun()

st.title("Bangers Softball Stats")

# --- Load ---
CURRENT_SEASON = get_current_season()
LAST_SEASON = get_last_season()
SEASON_ORDER = get_season_order()

season_stats = load_season_stats()
career_summary = load_career_stats().sort_values(["avg", "obp"], ascending=False)

season_summary = (
    season_stats[season_stats["season_id"] == CURRENT_SEASON]
    .sort_values(["avg", "obp"], ascending=False)
)

season_rec = load_season_record(CURRENT_SEASON)
alltime_rec = load_alltime_record()

sr = season_rec.iloc[0]
ar = alltime_rec.iloc[0]

st.markdown(
    f"## Season Record: {int(sr['wins'])}–{int(sr['losses'])}–{int(sr['draws'])} "
    f"({sr['win_pct']:.3f})"
)
st.markdown(
    f"<span style='color:gray; font-size:0.9rem;'>All-Time Record: "
    f"{int(ar['wins'])}–{int(ar['losses'])}–{int(ar['draws'])} "
    f"({ar['win_pct']:.3f})</span>",
    unsafe_allow_html=True,
)

# Career ranks (1 = best)
career_summary["AVG_Rank"] = career_summary["avg"].rank(ascending=False, method="min").astype(int)
career_summary["OBP_Rank"] = career_summary["obp"].rank(ascending=False, method="min").astype(int)
career_summary["H_Rank"] = career_summary["h"].rank(ascending=False, method="min").astype(int)
career_summary["GP_Rank"] = career_summary["gp"].rank(ascending=False, method="min").astype(int)

# Batting order: current roster, sorted by last season's AVG/OBP, newcomers at bottom
last_season_stats = season_stats[season_stats["season_id"] == LAST_SEASON]
current_roster = load_current_roster(CURRENT_SEASON)

batting_order = (
    current_roster
    .merge(last_season_stats[["player_name", "avg", "obp"]], on="player_name", how="left")
    .sort_values(["avg", "obp"], ascending=False, na_position="last")
)

# --- Tabs ---
tab_season_stats, tab_career_stats, tab_player_profile, tab_batting_order, tab_team_record = st.tabs([
    "Season Stats", "Career Stats", "Player Profile", "Batting Order", "Team Record"
])

with tab_season_stats:
    st.subheader("Season Stats")
    st.dataframe(
        season_summary.drop(columns=["season_id", "sort_order"]),
        use_container_width=True,
        column_config=STAT_COLUMN_CONFIG,
        hide_index=True,
    )

with tab_career_stats:
    st.subheader("Career Stats")
    st.dataframe(
        career_summary.drop(columns=["AVG_Rank", "OBP_Rank", "H_Rank", "GP_Rank"]),
        use_container_width=True,
        column_config=STAT_COLUMN_CONFIG,
        hide_index=True,
    )

with tab_player_profile:
    st.subheader("Player Profile")

    player = st.selectbox("Select a player", sorted(career_summary["player_name"].unique()))

    p = career_summary[career_summary["player_name"] == player].iloc[0]
    total_players = len(career_summary)

    photo_col, info_col = st.columns([1, 4], vertical_alignment="center")
    with photo_col:
        st.image(player_photo_path(player), width=140)
    with info_col:
        st.markdown(f"### {player}")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Games Played", int(p["gp"]), f"#{p['GP_Rank']} of {total_players}", delta_color="off")
        k2.metric("AVG", f"{p['avg']:.3f}", f"#{p['AVG_Rank']} of {total_players}", delta_color="off")
        k3.metric("OBP", f"{p['obp']:.3f}", f"#{p['OBP_Rank']} of {total_players}", delta_color="off")
        k4.metric("Hits", int(p["h"]), f"#{p['H_Rank']} of {total_players}", delta_color="off")

    player_history = season_by_season = season_stats[season_stats["player_name"] == player].copy()
    player_history = player_history.sort_values("sort_order")
    player_history["season_id"] = pd.Categorical(
        player_history["season_id"], categories=SEASON_ORDER, ordered=True
    )
    player_history["Career AVG"] = p["avg"]
    player_history = player_history.sort_values("season_id")

    st.line_chart(player_history, x="season_id", y=["avg", "Career AVG"])

    st.markdown("#### Batting Average by Opponent")
    vs_opponent = load_player_vs_opponent(player)

    st.dataframe(
        vs_opponent,
        use_container_width=True,
        hide_index=True,
        column_config={
            "opponent": "Opponent",
            "games_played": "GP",
            "ab": "AB",
            "h": "H",
            "bb": "BB",
            "sf": "SF",
            "avg": st.column_config.NumberColumn("AVG", format="%.3f"),
            "obp": st.column_config.NumberColumn("OBP", format="%.3f"),
        },
    )

    st.dataframe(
        player_history.drop(columns=["player_name", "sort_order"]),
        use_container_width=True,
        hide_index=True,
        column_config=STAT_COLUMN_CONFIG,
    )

with tab_batting_order:
    st.subheader("Batting Order")
    st.caption(f"Returning players sorted by {LAST_SEASON} AVG. New players at the bottom.")
    st.dataframe(
        batting_order,
        column_config=STAT_COLUMN_CONFIG,
        use_container_width=True,
        hide_index=True,
    )

with tab_team_record:
    st.subheader("Record by Opponent")
    team_record = load_team_record_by_opponent()
    st.dataframe(
        team_record,
        use_container_width=True,
        hide_index=True,
        column_config={
            "opponent": "Opponent",
            "wins": "Wins",
            "losses": "Losses",
            "draws": "Draws",
            "win_pct": st.column_config.NumberColumn("Win %", format="%.3f"),
        },
    )