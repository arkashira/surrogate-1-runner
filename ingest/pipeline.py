import re
from datetime import datetime
from typing import Dict, Any, List
import json
import logging
from . import schema

logger = logging.getLogger(__name__)

class FinancialTagExtractor:
    """Extracts revenue/expense metadata from cloud infrastructure logs"""
    
    REVENUE_PATTERN = re.compile(r'(?i)(revenue|income):?\s?(\$?\d+[\d,.]*)')
    EXPENSE_PATTERN = re.compile(r'(?i)(expense|cost):?\s?(\$?\d+[\d,.]*)')
    
    def __init__(self):
        self.error_count = 0
        self.total_processed = 0
        
    def extract_financial_tags(self, log_line: str) -> Dict[str, Any]:
        """Extract and normalize financial metadata with strict error handling"""
        try:
            self.total_processed += 1
            tags = {}
            
            # Extract revenue information
            revenue_match = self.REVENUE_PATTERN.search(log_line)
            if revenue_match:
                amount_str = revenue_match.group(2).replace('$', '').replace(',', '')
                tags['revenue'] = float(amount_str)
                
            # Extract expense information
            expense_match = self.EXPENSE_PATTERN.search(log_line)
            if expense_match:
                amount_str = expense_match.group(2).replace('$', '').replace(',', '')
                tags['expense'] = float(amount_str)
                
            # Add processing metadata
            tags['extracted_at'] = datetime.utcnow().isoformat()
            tags['source_type'] = 'cloud_infrastructure'
            
            return tags
            
        except Exception as e:
            self.error_count += 1
            logger.error(f"Failed to extract financial tags: {str(e)} - Line: {log_line[:200]}...")
            return {
                'error': str(e),
                'raw_line': log_line[:500],
                'extracted_at': datetime.utcnow().isoformat()
            }

class IngestPipeline:
    """Main ingestion pipeline with financial metadata integration"""
    
    def __init__(self):
        self.financial_extractor = FinancialTagExtractor()
        
    def process_batch(self, log_batch: List[str]) -> List[Dict[str, Any]]:
        """Process batch with financial metadata extraction and validation"""
        results = []
        
        for log_line in log_batch:
            # Extract financial tags
            financial_tags = self.financial_extractor.extract_financial_tags(log_line)
            
            # Validate against schema
            try:
                schema.validate(financial_tags)
                results.append(financial_tags)
            except schema.ValidationError as ve:
                logger.warning(f"Schema validation failed: {str(ve)}")
                results.append({
                    **financial_tags,
                    'validation_error': str(ve)
                })
                
        return results