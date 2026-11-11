CREATE TABLE customers (
    customer_id VARCHAR(10) PRIMARY KEY,
    customer_name NVARCHAR(100) NOT NULL,
    email NVARCHAR(255) UNIQUE,
    phone VARCHAR(20),
    city NVARCHAR(100),
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);

CREATE TABLE vehicles (
    vehicle_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10) NOT NULL,
    registration_number VARCHAR(20) UNIQUE NOT NULL,
    brand NVARCHAR(50) NOT NULL,
    model NVARCHAR(100) NOT NULL,
    battery_capacity DECIMAL(6,2) NOT NULL,
    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


CREATE TABLE charging_stations (
    station_id VARCHAR(10) PRIMARY KEY,
    station_name NVARCHAR(150) NOT NULL,
    city NVARCHAR(100) NOT NULL,
    latitude DECIMAL(9,6) NOT NULL,
    longitude DECIMAL(9,6) NOT NULL,
    total_chargers INT NOT NULL,

    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT CHK_station_latitude
        CHECK (latitude BETWEEN -90 AND 90),

    CONSTRAINT CHK_station_longitude
        CHECK (longitude BETWEEN -180 AND 180),

    CONSTRAINT CHK_total_chargers
        CHECK (total_chargers > 0)
);

CREATE TABLE charging_sessions (
    session_id VARCHAR(10) PRIMARY KEY,
    vehicle_id VARCHAR(10) NOT NULL,
    station_id VARCHAR(10) NOT NULL,
    start_time DATETIME2 NOT NULL,
    end_time DATETIME2,
    energy_consumed_kwh DECIMAL(10,3) NOT NULL DEFAULT 0,
    session_status VARCHAR(20) NOT NULL,

    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT FK_sessions_vehicles
        FOREIGN KEY (vehicle_id)
        REFERENCES vehicles(vehicle_id),

    CONSTRAINT FK_sessions_stations
        FOREIGN KEY (station_id)
        REFERENCES charging_stations(station_id),

    CONSTRAINT CHK_session_energy
        CHECK (energy_consumed_kwh >= 0),

    CONSTRAINT CHK_session_status
        CHECK (session_status IN
            ('Started', 'Completed', 'Cancelled', 'Failed')),

    CONSTRAINT CHK_session_time
        CHECK (end_time IS NULL OR end_time >= start_time)
);

CREATE TABLE transactions (
    transaction_id VARCHAR(10) PRIMARY KEY,
    session_id VARCHAR(10) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30) NOT NULL,
    payment_status VARCHAR(20) NOT NULL,

    transaction_timestamp DATETIME2 NOT NULL
        DEFAULT SYSUTCDATETIME(),

    created_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    updated_at DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT FK_transactions_sessions
        FOREIGN KEY (session_id)
        REFERENCES charging_sessions(session_id),

    CONSTRAINT CHK_transaction_amount
        CHECK (amount > 0),

    CONSTRAINT CHK_transaction_type
        CHECK (transaction_type IN ('Payment', 'Refund')),

    CONSTRAINT CHK_payment_status
        CHECK (payment_status IN
            ('Pending', 'Success', 'Failed'))
);

-- Table Names -- 
SELECT
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_TYPE = 'BASE TABLE'
  AND TABLE_SCHEMA = 'dbo'
ORDER BY TABLE_NAME;

-- Inspect the foreign key relationships--
SELECT
    OBJECT_NAME(fk.parent_object_id) AS child_table,
    COL_NAME(
        fkc.parent_object_id,
        fkc.parent_column_id
    ) AS child_column,
    OBJECT_NAME(fk.referenced_object_id) AS parent_table,
    COL_NAME(
        fkc.referenced_object_id,
        fkc.referenced_column_id
    ) AS parent_column
FROM sys.foreign_keys fk
JOIN sys.foreign_key_columns fkc
    ON fk.object_id = fkc.constraint_object_id
ORDER BY child_table;
