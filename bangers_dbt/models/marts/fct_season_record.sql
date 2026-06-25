with record as(
    select *
    from {{ ref('int_game_results') }}
),

wld as (
select 
    season_id,
    countif(result = 'W') as wins,
    countif(result = 'L') as losses,
    countif(result = 'D') as draws,
    sum(run_differential) as run_differential,
    avg(run_differential) as avg_run_differential
from record
group by season_id
)

select 
    season_id,
    wins,
    losses,
    draws,
    safe_divide(wins + (draws * 0.5), wins + losses + draws) as win_pct,
    run_differential,
    avg_run_differential
from wld