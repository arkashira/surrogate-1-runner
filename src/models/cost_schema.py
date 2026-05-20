import json
from typing import Any, Dict

class CostSchema:
    SCHEMA_VERSION = "1.0"
    
    @staticmethod
    def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a cost record to a common schema with default values.
        
        Args:
            record (Dict[str, Any]): The original cost record.
            
        Returns:
            Dict[str, Any]: The normalized cost record with guaranteed fields.
        """
        return {
            "provider": record.get("provider", ""),
            "service": record.get("service", ""),
            "resource_id": record.get("resource_id", ""),
            "amount_usd": record.get("amount_usd", 0.0),
            "timestamp": record.get("timestamp", ""),
            "schema_version": CostSchema.SCHEMA_VERSION
        }

    @staticmethod
    def validate_record(normalized_record: Dict[str, Any]) -> bool:
        """
        Validate if a normalized record conforms to the schema.
        
        Args:
            normalized_record (Dict[str, Any]): The normalized cost record.
            
        Returns:
            bool: True if the record is valid, False otherwise.
        """
        required_fields = ["provider", "service", "resource_id", "amount_usd", "timestamp", "schema_version"]
        return all(field in normalized_record for field in required_fields)

    @staticmethod
    def load_cost_data(file_path: str) -> Dict[str, Any]:
        """
        Load and normalize cost data from a JSON file.
        
        Args:
            file_path (str): Path to the JSON file containing cost data.
            
        Returns:
            Dict[str, Any]: The normalized cost record.
        """
        with open(file_path, 'r') as file:
            raw_data = json.load(file)
        return CostSchema.normalize_record(raw_data)

# Example usage:
# record = {"provider": "aws", "service": "s3", "resource_id": "res123", "amount_usd": 100.0, "timestamp": "2023-01-01T00:00:00Z"}
# normalized_record = CostSchema.normalize_record(record)
# print(CostSchema.validate_record(normalized_record))
# loaded_record = CostSchema.load_cost_data("cost_data.json")