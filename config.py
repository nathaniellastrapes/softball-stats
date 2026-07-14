from pathlib import Path

STAT_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10y8Y4PVAjfT8II6cI8BQqh3Qgqtajkra12OB4ALkzMw/export?format=csv&gid=225791941'


# Project root: .../softball-stats
BASE_DIR = Path(__file__).resolve().parents[0]

# Data paths
DATA_RAW = BASE_DIR / "data" / "raw" / "softball_stats_raw.csv"
DATA_PROCESSED = BASE_DIR / "data" / "processed" / "softball_stats_clean.parquet"
ACTIVE_ROSTER = BASE_DIR / "data" / "roster" / "active_roster.csv"

# Logo path
LOGO_PATH = BASE_DIR / "assets" / "bangers_logo.png"
