select
    session_id,
    vehicle_id,
    station_id,
    start_time,
    end_time,
    energy_consumed_kwh,
    session_status,
    created_at,
    updated_at
from {{ source('silver', 'charging_sessions') }}