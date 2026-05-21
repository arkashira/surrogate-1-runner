import json
import logging
from datetime import datetime
from typing import Dict, Any

class AuditLogger:
    def __init__(self, log_file: str = "audit_trail.log"):
        self.logger = logging.getLogger("audit")
        self.logger.setLevel(logging.INFO)
        
        # Create file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        # Add handler to logger
        self.logger.addHandler(file_handler)
    
    def log_ai_request(self, user_id: str, ai_tool: str, request_data: Dict[str, Any]):
        """Log an AI request with audit trail information"""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "ai_tool": ai_tool,
            "request_data": request_data
        }
        
        self.logger.info(json.dumps(audit_entry))

# Global audit logger instance
audit_logger = AuditLogger()

def log_ai_request(user_id: str, ai_tool: str, request_data: Dict[str, Any]):
    """Convenience function to log AI requests"""
    audit_logger.log_ai_request(user_id, ai_tool, request_data)