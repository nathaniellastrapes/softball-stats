def aggregate_stats(stats_df):
    stats_df = stats_df.assign(
        SeasonGame=stats_df["Season"].astype(str) + "_" + stats_df["Game"].astype(str)
    )
    
    agg = stats_df.groupby("PlayerName").agg(
        Games_Played=("SeasonGame", "nunique"),
        AB=("AB", "sum"),
        H=("H", "sum"),
        BB=("BB", "sum"),
        SF=("SF", "sum")
    )

    agg['AVG'] = (agg['H'] / agg['AB']).round(3)
    agg['OBP'] = ((agg["H"] + agg["BB"]) / (agg["AB"] + agg["BB"] + agg["SF"])).round(3)

    agg = agg.sort_values(by=['AVG', 'OBP', 'AB'], ascending=False)
    return agg.reset_index()