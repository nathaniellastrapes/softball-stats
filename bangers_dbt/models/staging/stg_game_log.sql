with source as (
    select *
    from {{ source('raw', 'game_log')}}
)

select 
    season_id,
    game,
    opponent,
    bangers_score,
    opponent_score
from source