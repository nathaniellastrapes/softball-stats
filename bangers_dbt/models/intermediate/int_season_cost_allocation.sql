with roster_counts as 
(
select 
    season_id,
    count(player_name) as player_count
from {{ ref('stg_season_roster') }}
group by season_id
)

select 
    a.season_id,
    a.league_fee,
    a.num_games,
    a.umpire_fee,
    a.playoff_umpire_fee,
    a.non_resident_fee,
    b.player_count,
    round(safe_divide(a.league_fee, b.player_count), 2) as league_share,
    round(safe_divide(a.umpire_fee, b.player_count), 2) as umpire_share,
    round(safe_divide(a.playoff_umpire_fee, b.player_count), 2) as playoff_share
from {{ ref('stg_season_costs') }} a
join roster_counts b on a.season_id = b.season_id