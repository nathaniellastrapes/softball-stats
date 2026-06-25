with results as(
    select *
    from {{ ref('stg_game_log')}}
)

select 
    season_id,
    game,
    opponent,
    bangers_score,
    opponent_score,
    case 
        when bangers_score > opponent_score then 'W'
        when bangers_score = opponent_score then 'D'
        else 'L'
    end as result,
    bangers_score - opponent_score as run_differential
from results