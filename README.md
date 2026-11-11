# EV Charging & Fleet Intelligence Platform

**An End-to-End Azure Data Engineering Solution for EV Charging Operations, Fleet Analytics, and Real-Time IoT Data Processing**

## Overview

The EV Charging & Fleet Intelligence Platform is an end-to-end data engineering solution designed to integrate and process data from an electric vehicle charging ecosystem.

The platform consolidates operational data from customers, vehicles, charging stations, charging sessions, and payment transactions, alongside external reference data and real-time IoT telemetry.

Built using Microsoft Azure, Azure Databricks, PySpark, Delta Lake, and dbt, the solution implements a scalable data architecture to support reliable batch and streaming data processing, historical data tracking, and business intelligence.

The platform follows the **Medallion Architecture (Bronze, Silver, and Gold)** to transform raw source data into trusted, analytics-ready datasets.

## Business Problem

EV charging operators generate large volumes of data across operational databases, charging stations, payment systems, and IoT devices.

Managing these independent data sources creates challenges such as:

- Lack of a unified view of charging operations.
- Difficulty tracking charging station utilization and availability.
- Limited visibility into energy consumption and revenue trends.
- Challenges processing high-volume IoT telemetry.
- Inconsistent data quality across operational systems.
- Difficulty maintaining historical records when source data changes.

This platform addresses these challenges by implementing a centralized data pipeline that supports batch ingestion, real-time processing, data transformation, and analytical reporting.

## Architecture

```text
                     DATA SOURCES
                          |
        +-----------------+------------------+
        |                 |                  |
    Azure SQL          REST APIs          IoT Devices
 Operational Data   External Reference    Telemetry
        |                 |                  |
        +-----------------+                  |
                  |                           |
          Azure Data Factory           Azure Event Hubs
           Batch Ingestion            Streaming Ingestion
                  |                           |
                  +-------------+-------------+
                                |
                         ADLS Gen2
                          Data Lake
                                |
                       Azure Databricks
                      PySpark + Delta Lake
                                |
                       MEDALLION ARCHITECTURE
                                |
                 +--------------+--------------+
                 |              |              |
               BRONZE         SILVER          GOLD
              Raw Data     Cleansed Data   Business Data
                 |              |              |
                 +--------------+--------------+
                                |
                             dbt Core
                     SQL Transformations & Tests
                                |
                        Databricks SQL
                                |
                            Power BI
                         BI Dashboards

       Governance: Unity Catalog | Secrets: Azure Key Vault
       Orchestration: ADF | Databricks Jobs / Workflows
       CI/CD: GitHub Actions
```

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Languages | Python, SQL |
| Cloud Platform | Microsoft Azure |
| Batch Ingestion | Azure Data Factory |
| Streaming Ingestion | Azure Event Hubs |
| Data Lake | Azure Data Lake Storage Gen2 |
| Data Processing | Azure Databricks, PySpark |
| Data Storage Format | Delta Lake |
| Data Architecture | Medallion Architecture |
| Data Transformation | dbt Core |
| Orchestration | Azure Data Factory, Databricks Jobs |
| Governance | Unity Catalog |
| Secrets Management | Azure Key Vault |
| Analytics | Databricks SQL, Power BI |
| Version Control | Git, GitHub |
| CI/CD | GitHub Actions |
| Containerization | Docker |

## Data Sources

The platform integrates data from three primary source categories.

### 1. Operational Data – Azure SQL Database

Relational operational data is maintained in Azure SQL Database.

| Table | Description |
|---|---|
| customers | Customer information and location details |
| vehicles | EV details, ownership, and battery specifications |
| charging_stations | Charging station locations, capacity, and operational status |
| charging_sessions | Charging activity, energy consumption, and session details |
| transactions | Payment transactions and payment status |

Incremental extraction is performed using source modification timestamps and watermark-based processing.

### 2. External Data – REST APIs

External reference data is ingested to enrich charging and operational datasets.

Examples include:

- Weather information.
- Electricity pricing.
- Charging station reference information.

### 3. IoT Telemetry – Azure Event Hubs

Simulated charging station telemetry is generated and streamed through Azure Event Hubs.

Telemetry attributes include:

- Station ID and connector ID.
- Voltage and current.
- Power consumption.
- Charging status.
- Event timestamp.

This data supports real-time processing and operational monitoring.

## Data Engineering Implementation

### 1. Batch Data Ingestion – Azure Data Factory

Implemented parameterized Azure Data Factory pipelines to ingest operational data from Azure SQL Database into ADLS Gen2.

Key implementation details:

- Configured linked services, datasets, and parameterized pipelines.
- Implemented metadata-driven ingestion for multiple source tables.
- Developed incremental loading using watermark-based extraction.
- Maintained ingestion metadata and processing status.
- Handled pipeline failures and supported reprocessing.

### 2. Data Lake Storage – ADLS Gen2

Azure Data Lake Storage Gen2 serves as the centralized storage layer.

Implemented a structured data organization strategy to store ingested source data and support downstream processing.

- Organized source data by domain and ingestion date.
- Maintained raw source data for historical reference.
- Separated ingestion and processing responsibilities.
- Integrated the data lake with Azure Databricks.

### 3. Bronze Layer – Raw Data Ingestion

The Bronze layer stores ingested source data in Delta format.

Key implementation details:

- Ingested batch data from ADLS Gen2.
- Captured streaming telemetry events.
- Preserved source-level attributes and ingestion metadata.
- Implemented incremental data ingestion.
- Maintained traceability between source records and ingested data.

### 4. Silver Layer – Data Cleansing and Transformation

The Silver layer applies data quality rules and standardization using PySpark and Delta Lake.

Key implementation details:

- Handled null values, duplicate records, and invalid data.
- Applied schema validation and data type standardization.
- Implemented business validation rules.
- Used Delta Lake MERGE for incremental upserts.
- Handled late-arriving and updated records.
- Implemented deduplication and data quality checks.

### 5. Gold Layer – Dimensional Modeling

The Gold layer contains business-ready datasets designed for analytical workloads.

Implemented dimensional modeling to support charging operations and fleet analytics.

**Dimension tables**

- `dim_customer`
- `dim_vehicle`
- `dim_station`
- `dim_date`

**Fact tables**

- `fact_charging_sessions`
- `fact_payments`
- `fact_station_telemetry`

Key implementation details:

- Designed fact and dimension tables using a star schema.
- Implemented surrogate key management.
- Applied Slowly Changing Dimension Type 2 (SCD Type 2) for historical tracking.
- Developed business-level aggregations.
- Prepared analytical datasets for reporting.

### 6. Real-Time Streaming – Azure Event Hubs and Spark Structured Streaming

Implemented a streaming pipeline to process simulated IoT telemetry generated by EV charging stations.

Key implementation details:

- Generated telemetry events using Python.
- Published events to Azure Event Hubs.
- Consumed streaming events using Spark Structured Streaming.
- Applied schema enforcement and data validation.
- Processed incoming telemetry incrementally.
- Used checkpoints to support streaming recovery.
- Stored processed telemetry in Delta tables.

### 7. Data Transformation – dbt Core

Implemented modular SQL transformations using dbt Core to organize and validate analytical datasets.

Key implementation details:

- Developed staging, intermediate, and mart models.
- Used reusable SQL transformations and model dependencies.
- Implemented schema and data quality tests.
- Configured dbt snapshots for historical change tracking.
- Organized transformations into maintainable model layers.

### 8. Pipeline Orchestration – Databricks Jobs and Azure Data Factory

Implemented orchestration across ingestion and transformation workflows.

- Used Azure Data Factory to schedule and manage source ingestion.
- Used Databricks Jobs / Workflows to orchestrate transformation tasks.
- Configured task dependencies and execution sequences.
- Implemented retry and failure-handling mechanisms.
- Managed batch and streaming workloads independently.

### 9. Governance and Security

Implemented data governance and security practices using Azure services.

- Used Unity Catalog for centralized data governance and access control.
- Integrated Azure Key Vault for secure credential management.
- Managed access to data and platform resources.
- Avoided hardcoding sensitive credentials in application code.

### 10. Analytics and Visualization – Power BI

Developed Power BI dashboards using business-ready datasets to provide visibility into EV charging operations.

**Key analytical areas**

| Dashboard Area | Business Metrics |
|---|---|
| Station Performance | Station utilization, availability, charging activity |
| Energy Consumption | Energy delivered, consumption trends |
| Revenue Analytics | Total revenue, payment status, transaction trends |
| Charging Sessions | Session volume, duration, energy per session |
| Fleet Analytics | Vehicle charging patterns and usage trends |
| IoT Monitoring | Telemetry trends and charging status |

## Data Quality and Reliability

The platform incorporates data quality and reliability practices across ingestion and transformation layers.

- Schema validation and enforcement.
- Null and duplicate record handling.
- Business rule validation.
- Incremental processing and idempotent upserts.
- Late-arriving data handling.
- Delta Lake transaction management.
- dbt data tests.
- Pipeline failure handling and recovery.

## Repository Structure

```text
ev-charging-intelligence/
│
├── data-generation/
│   ├── generate_customers.py
│   ├── generate_vehicles.py
│   ├── generate_stations.py
│   ├── generate_sessions.py
│   └── generate_telemetry.py
│
├── database/
│   ├── create_database.sql
│   ├── create_tables.sql
│   └── insert_sample_data.sql
│
├── azure-data-factory/
│   ├── pipelines/
│   ├── datasets/
│   └── linked-services/
│
├── databricks/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── streaming/
│
├── dbt/
│   ├── models/
│   │   ├── staging/
│   │   ├── intermediate/
│   │   └── marts/
│   ├── snapshots/
│   ├── tests/
│   └── dbt_project.yml
│
├── power-bi/
│   └── dashboards/
│
├── documentation/
│   ├── architecture.md
│   └── data_dictionary.md
│
├── .github/
│   └── workflows/
│
├── .gitignore
└── README.md
```

## Key Data Engineering Concepts Demonstrated

- End-to-end Azure Data Engineering.
- Metadata-driven and parameterized ingestion.
- Batch and streaming data pipelines.
- Watermark-based incremental loading.
- Medallion Architecture.
- PySpark transformations.
- Delta Lake MERGE and upsert operations.
- Deduplication and late-arriving data handling.
- Slowly Changing Dimension Type 2.
- Star schema and dimensional modeling.
- dbt models, tests, and snapshots.
- Workflow orchestration and error handling.
- Data governance and secrets management.
- CI/CD and version control.

## Business Outcomes

The platform provides a unified foundation for:

- Analyzing EV charging station utilization.
- Understanding energy consumption patterns.
- Monitoring charging session and payment performance.
- Evaluating fleet charging behavior.
- Processing IoT telemetry for operational visibility.
- Supporting data-driven decisions through analytical dashboards.

## Future Enhancements

- Implement predictive analytics for charging demand.
- Develop station-level energy demand forecasting.
- Introduce anomaly detection for charging station telemetry.
- Optimize charging station utilization through historical trends.

## Author

**Ajay**

**Project:** EV Charging & Fleet Intelligence Platform  
**Domain:** Electric Vehicle Charging and Fleet Operations  
**Focus:** Azure Data Engineering | PySpark | Databricks | Delta Lake | Batch & Streaming Processing | dbt | Power BI

---

*This project demonstrates the design and implementation of a modern cloud-based data engineering platform, covering the data lifecycle from source ingestion to business intelligence.*
