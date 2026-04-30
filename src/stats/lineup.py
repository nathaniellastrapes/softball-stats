import pandas as pd
from src.stats.batting import aggregate_stats
from config import LAST_SEASON

def build_batting_order(stats_df, roster_df):
    active_players = roster_df.loc[roster_df['IsActive'] == 1, "PlayerName"]

    last_season_df = stats_df[
        (stats_df['Season'] == LAST_SEASON)
        & (stats_df["PlayerName"].isin(active_players))]

    vets = aggregate_stats(last_season_df).sort_values(['AVG', 'OBP'], ascending=False)

    vet_names = set(vets["PlayerName"])
    new_names = [name for name in active_players if name not in vet_names]
    new_players = pd.DataFrame({"PlayerName": new_names})

    order = pd.concat([vets, new_players], ignore_index=True)
    return order[['PlayerName', 'AVG', 'OBP']]