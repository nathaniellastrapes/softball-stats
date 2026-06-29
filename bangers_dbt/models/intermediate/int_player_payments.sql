select 
    player_name,
    coalesce(sum(amount_paid), 0) as total_paid
from {{ ref('stg_payment_ledger') }}
group by 
    player_name