// Sample curated templates for the sidebar. In a real project these would be
// generated from the `templates/` directory and include metadata such as
// description, required parameters, and a unique id.
export const templates = [
  {
    id: 's3-to-parquet',
    name: 'S3 → Parquet',
    description: 'Streams data from an S3 bucket into a Parquet file.',
    parameters: ['s3Bucket', 'parquetPath'],
  },
  {
    id: 'gcs-to-jsonl',
    name: 'GCS → JSONL',
    description: 'Copies data from a GCS bucket into a JSONL file.',
    parameters: ['gcsBucket', 'jsonlPath'],
  },
  {
    id: 's3-to-csv',
    name: 'S3 → CSV',
    description: 'Exports data from S3 into a CSV file.',
    parameters: ['s3Bucket', 'csvPath'],
  },
  {
    id: 'gcs-to-parquet',
    name: 'GCS → Parquet',
    description: 'Streams data from GCS into a Parquet file.',
    parameters: ['gcsBucket', 'parquetPath'],
  },
  {
    id: 's3-to-jsonl',
    name: 'S3 → JSONL',
    description: 'Copies data from S3 into a JSONL file.',
    parameters: ['s3Bucket', 'jsonlPath'],
  },
];