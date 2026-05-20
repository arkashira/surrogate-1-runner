import csv
from typing import List, Dict, Any
from io import StringIO


def export_build_to_csv(build_data: List[Dict[str, Any]]) -> str:
    """
    Exports build component data to CSV format.
    
    Args:
        build_data: List of dictionaries containing component information
        
    Returns:
        CSV formatted string
    """
    if not build_data:
        return ""
        
    # Get all unique keys from all dictionaries to ensure consistent columns
    fieldnames = set()
    for item in build_data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))
    
    # Use StringIO to create an in-memory CSV file
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # Write header
    writer.writeheader()
    
    # Write data rows
    for item in build_data:
        writer.writerow(item)
    
    return output.getvalue()


def export_build_to_csv_file(build_data: List[Dict[str, Any]], filename: str) -> None:
    """
    Exports build component data to a CSV file.
    
    Args:
        build_data: List of dictionaries containing component information
        filename: Output file path
    """
    if not build_data:
        return
        
    # Get all unique keys from all dictionaries to ensure consistent columns
    fieldnames = set()
    for item in build_data:
        fieldnames.update(item.keys())
    fieldnames = sorted(list(fieldnames))
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for item in build_data:
            writer.writerow(item)