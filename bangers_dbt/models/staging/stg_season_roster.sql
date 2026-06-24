with source as (
    select *
    from {{ source('raw', 'season_roster')}}
)

select 
    season_id,
    player_name,
    resident_flag
from source