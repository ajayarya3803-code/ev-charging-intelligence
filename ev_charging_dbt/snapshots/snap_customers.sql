{% snapshot snap_customers %}

{{
    config(
        target_schema='snapshots',
        unique_key='customer_id',
        strategy='timestamp',
        updated_at='updated_at'
    )
}}

SELECT
    customer_id,
    customer_name,
    email,
    phone,
    city,
    created_at,
    updated_at
FROM {{ source('silver', 'customers') }}

{% endsnapshot %}