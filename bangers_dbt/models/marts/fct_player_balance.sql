with owed as (
select 
  player_name,
  sum(season_total_owed) as total_owed
from {{ ref('fct_player_season_charges') }}
group by player_name
)

select
  a.player_name,
  round(a.total_owed, 2) as total_owed,
  round(coalesce(b.total_paid, 0), 2) as total_paid,
  round(a.total_owed - coalesce(b.total_paid, 0), 2) as balance
from owed a
left join {{ ref('int_player_payments') }} b on a.player_name = b.player_name
