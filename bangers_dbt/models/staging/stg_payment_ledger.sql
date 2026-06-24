with source as (
    select *
    from {{ source('raw', 'payment_ledger')}}
)

select 
    season_id,
    player_name,
    amount_paid,
    payment_date,
    payment_method
from source