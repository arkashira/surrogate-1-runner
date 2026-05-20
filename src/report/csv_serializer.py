import csv
from io import StringIO
from typing import List, Dict

def serialize_to_csv(data: List[Dict[str, any]]) -> str:
    """
    Serializes a list of dictionaries into a CSV string.
    
    Args:
        data: A list of dictionaries where each dictionary represents a row in the CSV.
              Each dictionary should have keys corresponding to the column names.
              
    Returns:
        A string representing the CSV content.
    """
    if not data:
        return ""
    
    # Ensure all required columns are present in the data
    required_columns = ["month", "total_spend_usd", "spend_change_pct", "service", "service_spend_usd", "recommendation", "recommendation_savings_usd"]
    for item in data:
        if not all(key in item for key in required_columns):
            raise ValueError("Missing required columns in data.")
    
    # Create a StringIO object to write the CSV data into
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=required_columns)
    
    # Write the header row
    writer.writeheader()
    
    # Write the data rows
    writer.writerows(data)
    
    # Get the CSV content as a string
    csv_content = output.getvalue()
    
    # Close the StringIO object
    output.close()
    
    return csv_content

# Example usage:
# data = [
#     {
#         "month": "2023-01",
#         "total_spend_usd": 1000,
#         "spend_change_pct": 5.0,
#         "service": "AWS",
#         "service_spend_usd": 800,
#         "recommendation": "Optimize EC2 instances",
#         "recommendation_savings_usd": 200
#     },
#     # ... more data ...
# ]
# csv_data = serialize_to_csv(data)
# print(csv_data)