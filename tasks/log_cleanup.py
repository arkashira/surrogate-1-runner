import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/opt/axentx/surrogate-1/logs/system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def cleanup_old_logs():
    """Remove log entries older than 90 days from audit.jsonl"""
    
    log_file_path = '/opt/axentx/surrogate-1/logs/audit.jsonl'
    
    # Check if log file exists
    if not os.path.exists(log_file_path):
        logger.info("Audit log file does not exist, nothing to clean up")
        return
    
    # Read all lines from the log file
    try:
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        logger.error(f"Error reading audit log file: {e}")
        return
    
    # Filter out entries older than 90 days
    cutoff_date = datetime.now() - timedelta(days=90)
    filtered_lines = []
    
    for line in lines:
        try:
            entry = json.loads(line.strip())
            entry_date = datetime.fromisoformat(entry.get('timestamp', '').replace('Z', '+00:00'))
            
            if entry_date >= cutoff_date:
                filtered_lines.append(line)
            else:
                logger.debug(f"Removing old log entry: {entry}")
        except Exception as e:
            logger.warning(f"Skipping malformed log entry: {e}")
            # Keep malformed entries to avoid data loss
            filtered_lines.append(line)
    
    # Write back only the recent entries
    try:
        with open(log_file_path, 'w') as f:
            f.writelines(filtered_lines)
        logger.info(f"Cleaned up old log entries. {len(lines) - len(filtered_lines)} entries removed.")
    except Exception as e:
        logger.error(f"Error writing to audit log file: {e}")

if __name__ == "__main__":
    cleanup_old_logs()