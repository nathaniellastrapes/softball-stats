import pandas as pd
from config import DATA_RAW, ACTIVE_ROSTER


def load_stats():
    df = pd.read_csv(DATA_RAW)
    return df

def load_roster():
    df = pd.read_csv(ACTIVE_ROSTER)
    return df