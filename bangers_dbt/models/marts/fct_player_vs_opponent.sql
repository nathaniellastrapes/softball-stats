with player_games as (
    select
        pg.player_name,
        g.opponent,
        pg.ab,
        pg.h,
        pg.bb,
        pg.sf
    from {{ ref('fct_player_game') }} pg
    join {{ ref('int_game_results') }} g
        on pg.season_id = g.season_id and pg.game = g.game
),

agg as (
    select
        player_name,
        opponent,
        count(*) as games_played,
        sum(ab) as ab,
        sum(h) as h,
        sum(bb) as bb,
        sum(sf) as sf
    from player_games
    group by player_name, opponent
)

select
    player_name,
    opponent,
    games_played,
    ab,
    h,
    bb,
    sf,
    round(safe_divide(h, ab), 3) as avg,
    round(safe_divide(h + bb, ab + bb + sf), 3) as obp
from agg