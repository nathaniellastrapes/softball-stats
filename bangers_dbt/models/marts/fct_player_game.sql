with stats as (
    select *
    from {{ ref('stg_stat_log')}}
)

select 
    season_id,
    game,
    player_name,
    ab,
    h,
    bb,
    sf
from stats