select
    season_id,
    player_name,
    resident_flag
from {{ ref('stg_season_roster') }}