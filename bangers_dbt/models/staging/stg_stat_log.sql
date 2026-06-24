with source as (
    select *
    from {{ source('raw', 'stat_log')}}
)

select 
    season_id,
    game,
    player_name,
    ab,
    h,
    bb,
    sf
from source