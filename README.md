# etl_sales
Sales Data ETL Pipeline  A Python-based ETL pipeline that processes raw CSV data into a SQLite database.
Key Features:
- Data Cleaning: Handles encoding issues, removes nulls, and filters negative values.
- Data Integrity: Includes a Reconciliation Check to ensure input rows match output + dropped rows.
- Automated Logging:Tracks every step in `pipeline.log`.
