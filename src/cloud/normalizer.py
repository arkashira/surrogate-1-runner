import json
from typing import List, Dict, Any

SCHEMA_VERSION = "1.0"

def normalize_cost_data(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_records = []
    for record in records:
        normalized_record = {
            "provider": record.get("provider"),
            "service": record.get("service"),
            "resource_id": record.get("resource_id"),
            "amount_usd": record.get("amount_usd"),
            "timestamp": record.get("timestamp"),
            "schema_version": SCHEMA_VERSION
        }
        normalized_records.append(normalized_record)
    return normalized_records

def load_json_file(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json_file(file_path: str, data: List[Dict[str, Any]]) -> None:
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Example usage
    input_file = "input_data.json"
    output_file = "normalized_data.json"
    
    records = load_json_file(input_file)
    normalized_data = normalize_cost_data(records)
    save_json_file(output_file, normalized_data)