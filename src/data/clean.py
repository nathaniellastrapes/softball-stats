from config import CURRENT_SEASON

def filter_active_player_stats(stats_df, roster_df):
    active_players = roster_df.loc[roster_df['IsActive'] == 1, "PlayerName"]
    return stats_df[stats_df['PlayerName'].isin(active_players)]

def filter_current_season(stats_df, season=CURRENT_SEASON):
    season_stats = stats_df[stats_df['Season'] == season]
    return season_stats

# def filter_active_current_season(stats_df, roster_df, season=CURRENT_SEASON):
#     season_stats = stats_df[stats_df['Season'] == season]
#     active_players = roster_df.loc[roster_df['IsActive'] == 1, "PlayerName"]
#     return season_stats[season_stats['PlayerName'].isin(active_players)]
