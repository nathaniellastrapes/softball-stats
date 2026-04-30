from pathlib import Path

# Current Season
CURRENT_SEASON = "Spring2026"
LAST_SEASON = 'Winter2026'

# Project root: .../softball-stats
BASE_DIR = Path(__file__).resolve().parents[0]

# Data paths
DATA_RAW = BASE_DIR / "data" / "raw" / "softball_stats_raw.csv"
DATA_PROCESSED = BASE_DIR / "data" / "processed" / "softball_stats_clean.parquet"
ACTIVE_ROSTER = BASE_DIR / "data" / "roster" / "active_roster.csv"

# Logo path
LOGO_PATH = BASE_DIR / "assets" / "bangers_logo.png"