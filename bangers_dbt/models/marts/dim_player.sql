with player_info as (
    select *
    from {{ ref('stg_player_info') }}
)

select 
    player_name,
    player_number,
    nickname,
    jersey_size
from player_info