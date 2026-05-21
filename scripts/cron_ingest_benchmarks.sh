#!/bin/bash

# Define the script directory and log file
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
LOG_FILE="/var/log/axentx/surrogate-1/ingest_errors.log"

# Function to log errors
log_error() {
  echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to parse and ingest CSV files
parse_and_ingest_csv() {
  local csv_file="$1"
  
  # Check if the file exists
  if [ ! -f "$csv_file" ]; then
    log_error "CSV file not found: $csv_file"
    return 1
  fi
  
  # Parse the CSV file and insert into the database
  while IFS=',' read -r gpu cpu ram_gb fps date; do
    # Validate the row
    if [[ -z "$gpu" || -z "$cpu" || -z "$ram_gb" || -z "$fps" || -z "$date" ]]; then
      log_error "Invalid row in CSV: $gpu, $cpu, $ram_gb, $fps, $date"
      continue
    fi
    
    # Insert the valid row into the database
    psql -c "INSERT INTO benchmark_results (gpu, cpu, ram_gb, fps, date) VALUES ('$gpu', '$cpu', $ram_gb, $fps, '$date');"
  done < "$csv_file"
}

# Main script logic
find /data/benchmarks -type f -name "*.csv" -mmin -5 | while read -r csv_file; do
  parse_and_ingest_csv "$csv_file"
done

# Update the health metric
echo "benchmarks_last_ingest_timestamp $(date +%s)" > /metrics/benchmarks_last_ingest_timestamp