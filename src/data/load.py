import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery


@st.cache_resource
def get_client():
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"]
    )
    return bigquery.Client(credentials=credentials, project="bangers-warehouse")

@st.cache_data(ttl=600)
def run_query(query):
    client = get_client()
    return client.query(query).to_dataframe()

@st.cache_data(ttl=600)
def load_season_stats():
    return run_query("""
        select f.*, s.sort_order
        from `bangers-warehouse.dbt_dev.fct_player_season` f
        join `bangers-warehouse.dbt_dev.dim_season` s using (season_id)
    """)

@st.cache_data(ttl=600)
def load_career_stats():
    return run_query("""
        select c.*
        from `bangers-warehouse.dbt_dev.fct_player_career` c
        where c.player_name in (
            select player_name
            from `bangers-warehouse.dbt_dev.dim_season_roster`
            where season_id = (
                select season_id
                from `bangers-warehouse.dbt_dev.fct_player_season` f
                join `bangers-warehouse.dbt_dev.dim_season` s using (season_id)
                order by s.sort_order desc
                limit 1
            )
        )
    """)

@st.cache_data(ttl=600)
def get_current_season():
    df = run_query("""
                   select season_id 
                   from `bangers-warehouse.dbt_dev.dim_season` 
                   order by sort_order desc
                   limit 1""")
    return df['season_id'].iloc[0]

@st.cache_data(ttl=600)
def get_last_season():
    df = run_query("""
                   select season_id 
                   from `bangers-warehouse.dbt_dev.dim_season` 
                   order by sort_order desc 
                   limit 1
                   offset 1""")
    return df['season_id'].iloc[0]

@st.cache_data(ttl=600)
def get_season_order():
    df = run_query("""
        select season_id
        from `bangers-warehouse.dbt_dev.dim_season`
        order by sort_order
    """)
    return df["season_id"].tolist()

@st.cache_data(ttl=600)
def load_current_roster(season):
    return run_query(f"""
        select distinct player_name
        from `bangers-warehouse.dbt_dev.dim_season_roster`
        where season_id = '{season}'
    """)

@st.cache_data(ttl=600)
def load_season_record(season):
    return run_query(f"""
        select wins, losses, draws, win_pct
        from `bangers-warehouse.dbt_dev.fct_season_record`
        where season_id = '{season}'
    """)

@st.cache_data(ttl=600)
def load_alltime_record():
    return run_query("""
        select
            sum(wins) as wins,
            sum(losses) as losses,
            sum(draws) as draws,
            safe_divide(sum(wins) + 0.5 * sum(draws), sum(wins) + sum(losses) + sum(draws)) as win_pct
        from `bangers-warehouse.dbt_dev.fct_season_record`
    """)

@st.cache_data(ttl=600)
def load_team_record_by_opponent():
    return run_query("""
        select opponent, wins, losses, draws, win_pct
        from `bangers-warehouse.dbt_dev.fct_team_record`
        order by win_pct desc
    """)

@st.cache_data(ttl=600)
def load_player_vs_opponent(player):
    return run_query(f"""
        select opponent, games_played, ab, h, bb, sf, avg, obp
        from `bangers-warehouse.dbt_dev.fct_player_vs_opponent`
        where player_name = '{player}'
        order by avg desc
    """)