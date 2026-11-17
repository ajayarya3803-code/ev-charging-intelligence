select
    customer_id,
    customer_name,
    email,
    phone,
    city,
    created_at,
    updated_at
from {{ source('silver', 'customers') }}