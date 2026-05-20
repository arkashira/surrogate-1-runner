
# Data Pipeline Templates Directory

This directory contains pre-built pipeline templates for common data transformation tasks. Each template includes:

- Clear description of the transformation
- Required parameters with types and descriptions
- Version information

## Available Templates

1. **S3 to Parquet** (`s3_to_parquet.yaml`)
   - Converts data from S3 bucket to Parquet format
   - Supports prefix filtering

2. **GCS to JSONL** (`gcs_to_jsonl.yaml`)
   - Converts data from GCS bucket to JSONL format
   - Supports prefix filtering

3. **MySQL to Avro** (`mysql_to_avro.yaml`)
   - Exports MySQL table data to Avro format
   - Requires database credentials

4. **PostgreSQL to CSV** (`postgres_to_csv.yaml`)
   - Exports PostgreSQL table data to CSV format
   - Requires database credentials

5. **Kafka to Parquet** (`kafka_to_parquet.yaml`)
   - Consumes Kafka topic data and writes to Parquet
   - Requires broker configuration

## Usage Instructions

1. Copy the desired template into your pipeline configuration
2. Fill in all required parameters
3. Execute the pipeline

All templates follow the same parameter naming conventions and use standard data formats for compatibility.