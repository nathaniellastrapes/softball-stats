with source as (
    select *
    from {{ source('raw', 'player_info')}}
)

select 
    player_name,
    player_number,
    nickname,
    jersey_size
from source