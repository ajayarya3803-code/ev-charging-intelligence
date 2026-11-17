select
    transaction_id,
    session_id,
    transaction_type,
    amount,
    payment_method,
    payment_status,
    transaction_timestamp,
    created_at,
    updated_at
from {{ ref('stg_transactions') }}