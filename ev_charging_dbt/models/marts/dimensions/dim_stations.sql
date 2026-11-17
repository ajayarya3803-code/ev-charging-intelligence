select
    station_id,
    station_name,
    city,
    latitude,
    longitude,
    total_chargers,
    created_at,
    updated_at
from {{ ref('stg_charging_stations') }}