with base as (
    select
        a.season_id,
        a.player_name,
        b.league_share,
        b.umpire_share,
        b.playoff_share,
        case when a.resident_flag = 1 then 0
            else b.non_resident_fee
        end as non_resident_fee
    from {{ ref('stg_season_roster') }} a
    join {{ ref('int_season_cost_allocation') }} b on a.season_id = b.season_id
)

select
    season_id,
    player_name,
    round(league_share, 2) as league_share,
    round(umpire_share, 2) as umpire_share,
    round(playoff_share, 2) as playoff_share,
    round(non_resident_fee, 2) as non_resident_fee,
    round(league_share + umpire_share + playoff_share + non_resident_fee, 2) as season_total_owed
from base