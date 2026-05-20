import csv
import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional

def export_logs(
    output_format: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    limit: Optional[int] = None
) -> None:
    """
    Export AI model access logs to specified format.
    
    Args:
        output_format: 'csv' or 'json'
        start_date: Start date in YYYY-MM-DD format (optional)
        end_date: End date in YYYY-MM-DD format (optional)
        limit: Maximum number of logs to export (optional)
    """
    # Define log file path - assuming logs are stored in this directory
    log_file = "access_logs.json"
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading logs: {e}")
        return

    # Filter logs by date range if provided
    filtered_logs = logs
    if start_date:
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]).date() >= start]
    
    if end_date:
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        filtered_logs = [log for log in filtered_logs if datetime.fromisoformat(log["timestamp"]).date() <= end]
    
    # Apply limit if specified
    if limit and len(filtered_logs) > limit:
        filtered_logs = filtered_logs[:limit]

    # Export based on format
    if output_format == "csv":
        export_csv(filtered_logs)
    elif output_format == "json":
        export_json(filtered_logs)
    else:
        print("Invalid format. Use 'csv' or 'json'.")

def export_csv(logs: List[Dict]) -> None:
    """Export logs to CSV format."""
    if not logs:
        print("No logs to export.")
        return
    
    # Determine columns from first log entry
    fieldnames = logs[0].keys()
    
    output_file = "access_logs.csv"
    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(logs)
        print(f"Successfully exported {len(logs)} logs to {output_file}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

def export_json(logs: List[Dict]) -> None:
    """Export logs to JSON format."""
    if not logs:
        print("No logs to export.")
        return
    
    output_file = "access_logs.json"
    try:
        with open(output_file, 'w') as f:
            json.dump(logs, f, indent=2)
        print(f"Successfully exported {len(logs)} logs to {output_file}")
    except Exception as e:
        print(f"Error writing JSON: {e}")

def main():
    parser = argparse.ArgumentParser(description="Export AI model access logs")
    parser.add_argument(
        "--format", 
        choices=["csv", "json"],
        required=True,
        help="Export format (csv or json)"
    )
    parser.add_argument(
        "--start-date",
        help="Start date (YYYY-MM-DD, optional)"
    )
    parser.add_argument(
        "--end-date",
        help="End date (YYYY-MM-DD, optional)"
    )
    parser.add_argument(
        "--limit",
        type=int,
        help="Maximum number of logs to export (optional)"
    )
    
    args = parser.parse_args()
    export_logs(
        output_format=args.format,
        start_date=args.start_date,
        end_date=args.end_date,
        limit=args.limit
    )

if __name__ == "__main__":
    main()