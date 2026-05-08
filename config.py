from pathlib import Path

STAT_SHEET_URL = 'https://docs.google.com/spreadsheets/d/10y8Y4PVAjfT8II6cI8BQqh3Qgqtajkra12OB4ALkzMw/export?format=csv&gid=225791941'

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

# Season order 
SEASON_ORDER = [
    "Winter2023", "Spring2023", "Summer2023", "Fall2023",
    "Winter2024", "Spring2024", "Summer2024", "Fall2024",
    "Winter2025", "Spring2025", "Summer2025", "Fall2025",
    "Winter2026", "Spring2026", "Summer2026", "Fall2026",
]