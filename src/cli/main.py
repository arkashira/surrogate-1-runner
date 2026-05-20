import uuid
import sqlite3
import json
import csv
from datetime import datetime

def generate_report_id():
    return str(uuid.uuid4())

def persist_metadata(report_id, timestamp, repo_name, user_id):
    conn = sqlite3.connect('/opt/axentx/surrogate-1/data/scans.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scans (
            id TEXT PRIMARY KEY,
            timestamp TEXT,
            repo_name TEXT,
            user_id TEXT
        )
    ''')
    cursor.execute('INSERT INTO scans VALUES (?, ?, ?, ?)', (report_id, timestamp, repo_name, user_id))
    conn.commit()
    conn.close()

def save_scan_results(report_id, results, format='json'):
    if format == 'json':
        with open(f'report_{report_id}.json', 'w') as f:
            json.dump(results, f)
    elif format == 'csv':
        with open(f'report_{report_id}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(results.keys())
            writer.writerow(results.values())

def perform_scan(repo_name, user_id):
    report_id = generate_report_id()
    timestamp = datetime.now().isoformat()
    results = {'repo': repo_name, 'user': user_id}  # Placeholder for actual scan results
    
    persist_metadata(report_id, timestamp, repo_name, user_id)
    save_scan_results(report_id, results, format='json')
    save_scan_results(report_id, results, format='csv')

def list_scans(user_id):
    conn = sqlite3.connect('/opt/axentx/surrogate-1/data/scans.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM scans WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Perform a scan and manage scan history.')
    subparsers = parser.add_subparsers(dest='command')

    scan_parser = subparsers.add_parser('scan', help='Perform a scan')
    scan_parser.add_argument('--repo', required=True, help='Repository name')
    scan_parser.add_argument('--user', required=True, help='User ID')

    history_parser = subparsers.add_parser('history', help='List past scans')
    history_parser.add_argument('--user', required=True, help='User ID')

    args = parser.parse_args()

    if args.command == 'scan':
        perform_scan(args.repo, args.user)
    elif args.command == 'history':
        scans = list_scans(args.user)
        for scan in scans:
            print(scan)