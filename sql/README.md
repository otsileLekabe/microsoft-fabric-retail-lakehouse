# Microsoft Fabric – RetailLakehouse (Medallion Architecture)

## Project Overview
An end-to-end data engineering pipeline built in Microsoft Fabric using PySpark, Delta Lake, and T-SQL to ingest raw retail point-of-sale data into a Bronze/Silver Lakehouse architecture with automated quality checks.

## Architecture Flow
```text
Raw CSV (Files/raw) ──▶ Bronze Delta Table (Raw Ingestion) ──▶ Silver Delta Table (Validated & Cleaned) ──▶ SQL Analytics Endpoint
```

## Automated Data Quality Rules (Bronze ➔ Silver)
1. **Primary Key Enforcement:** Filters out records with `NULL` `transaction_id` values.
2. **Deduplication:** Removes duplicate transaction events (`TXN-9002`).
3. **Domain Validation:** Rejects transactions with `quantity <= 0` or `unit_price <= 0`.
4. **Text Standardization:** Normalizes inconsistent casing in `status` (`"completed"`, `"COMPLETED"` ➔ `"Completed"`).

## Repository Structure
* `data/sample_retail_raw.csv`: Raw point-of-sale dataset containing intentional anomalies to test pipeline validation.
* `notebooks/01_ingest_to_bronze.py`: PySpark script ingesting raw CSV data into `bronze_retail_sales` Delta table.
* `notebooks/02_transform_silver.py`: PySpark transformation script applying data quality checks and writing to `silver_retail_sales`.
* `sql/silver_analytics_queries.sql`: T-SQL reporting queries designed for the Fabric SQL Analytics Endpoint.
