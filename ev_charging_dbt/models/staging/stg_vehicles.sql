select
    vehicle_id,
    customer_id,
    registration_number,
    brand,
    model,
    battery_capacity,
    created_at,
    updated_at
from {{ source('silver', 'vehicles') }}