with season_stats as (
    select 
        season_id,
        player_name,
        sum(ab) as ab,
        sum(h) as h,
        sum(bb) as bb,
        sum(sf) as sf
    from {{ ref('fct_player_game' )}}
    group by 
        season_id,
        player_name
)

select
    season_id,
    player_name,
    ab, 
    h, 
    bb, 
    sf,
    round(safe_divide(h, ab), 3) as avg,
    round(safe_divide(h + bb, ab + bb + sf), 3) as obp
from season_stats
