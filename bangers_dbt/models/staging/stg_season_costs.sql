with source as (
    select *
    from {{ source('raw', 'season_costs')}}
)

select 
    season_id,
    league_fee,
    num_games,
    umpire_rate,
    umpire_fee,
    playoff_umpire_fee,
    non_resident_fee
from source