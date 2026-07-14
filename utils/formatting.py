# utils/formatting.py
import streamlit as st
from pathlib import Path
from config import BASE_DIR

PLAYER_PHOTO_DIR = BASE_DIR / "assets" / "players"
PLACEHOLDER_PHOTO = PLAYER_PHOTO_DIR / "_placeholder.jpg"

def player_photo_path(player_name):
    """Return the path to a player's photo, or the placeholder if missing."""
    slug = player_name.lower().replace(" ", "_")
    photo = PLAYER_PHOTO_DIR / f"{slug}.jpg"
    if photo.exists():
        return str(photo)
    # Try .png as a fallback
    photo_png = PLAYER_PHOTO_DIR / f"{slug}.png"
    if photo_png.exists():
        return str(photo_png)
    return str(PLACEHOLDER_PHOTO)

STAT_COLUMN_CONFIG = {
    "season_id": "Season",
    "player_name": "Player Name",
    "gp": "Games Played",
    "ab": "AB",
    "h": "H",
    "bb": "BB",
    "sf": "SF",
    "avg": st.column_config.NumberColumn("AVG", format="%.3f"),
    "obp": st.column_config.NumberColumn("OBP", format="%.3f"),
}