import json
from typing import Dict, List, Tuple

def load_results(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_transactions(mysql_results: Dict, mariadb_results: Dict) -> List[Tuple[str, Dict, Dict]]:
    differences = []
    for key in mysql_results.keys():
        if key in mariadb_results:
            if mysql_results[key] != mariadb_results[key]:
                differences.append((key, mysql_results[key], mariadb_results[key]))
        else:
            differences.append((key, mysql_results[key], None))
    
    for key in mariadb_results.keys():
        if key not in mysql_results:
            differences.append((key, None, mariadb_results[key]))
    
    return differences

def main(mysql_result_file: str, mariadb_result_file: str) -> None:
    mysql_results = load_results(mysql_result_file)
    mariadb_results = load_results(mariadb_result_file)
    
    differences = compare_transactions(mysql_results, mariadb_results)
    
    print("Detected differences:")
    for diff in differences:
        print(f"Key: {diff[0]}, MySQL Result: {diff[1]}, MariaDB Result: {diff[2]}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python compare_results.py <mysql_result_file> <mariadb_result_file>")
        sys.exit(1)
    
    mysql_result_file = sys.argv[1]
    mariadb_result_file = sys.argv[2]
    
    main(mysql_result_file, mariadb_result_file)