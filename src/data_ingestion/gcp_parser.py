import json
import logging
from pathlib import Path
from typing import Iterator, Dict, Any
from datetime import datetime

from src.models.cost_record import CostRecord

logger = logging.getLogger(__name__)

class GCPBillingParser:
    """Parses GCP billing export data into structured CostRecords."""
    
    def __init__(self):
        self._valid_fields = {
            'invoice', 'service', 'sku', 'usage_start_time', 'usage_end_time',
            'cost', 'currency', 'project', 'location', 'resource', 'labels'
        }
    
    def parse_file(self, file_path: Path) -> Iterator[CostRecord]:
        """
        Parse a GCP billing export JSON file and yield CostRecords.
        
        Args:
            file_path: Path to the GCP billing export JSON file
            
        Yields:
            CostRecord objects parsed from the file
        """
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
            # Handle both single record and array of records
            if isinstance(data, list):
                records = data
            else:
                records = [data]
                
            for record_data in records:
                try:
                    cost_record = CostRecord.from_gcp_export(record_data)
                    yield cost_record
                except Exception as e:
                    logger.warning(f"Skipping invalid record: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing GCP billing file {file_path}: {e}")
            raise
    
    def parse_stream(self, stream_data: str) -> Iterator[CostRecord]:
        """
        Parse streaming GCP billing data from a string.
        
        Args:
            stream_data: JSON string containing GCP billing data
            
        Yields:
            CostRecord objects parsed from the stream
        """
        try:
            data = json.loads(stream_data)
            
            # Handle both single record and array of records
            if isinstance(data, list):
                records = data
            else:
                records = [data]
                
            for record_data in records:
                try:
                    cost_record = CostRecord.from_gcp_export(record_data)
                    yield cost_record
                except Exception as e:
                    logger.warning(f"Skipping invalid record from stream: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing GCP billing stream: {e}")
            raise
    
    def validate_record(self, record_data: Dict[str, Any]) -> bool:
        """
        Validate that a record contains required fields.
        
        Args:
            record_data: Raw record data from GCP export
            
        Returns:
            True if record is valid, False otherwise
        """
        required_fields = ['invoice', 'service', 'sku', 'usage_start_time', 
                          'usage_end_time', 'cost', 'currency']
        
        for field in required_fields:
            if field not in record_data:
                return False
                
        # Additional validation for nested fields
        if not record_data['invoice'].get('month'):
            return False
            
        if not record_data['service'].get('description'):
            return False
            
        if not record_data['sku'].get('description'):
            return False
            
        return True