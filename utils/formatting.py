# utils/formatting.py
import streamlit as st
from pathlib import Path
from config import BASE_DIR

STAT_COLUMN_CONFIG = {
    "PlayerName": "Player Name",
    "Games_Played": "Games Played",
    "AVG": st.column_config.NumberColumn(format="%.3f"),
    "OBP": st.column_config.NumberColumn(format="%.3f"),
}


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