
import os
import logging
import psycopg2
import requests
from datetime import datetime, timedelta

# Set up logging
logging.basicConfig(filename='/var/log/axentx/cron-scout-audit/daily_scan.log', level=logging.INFO)

# Database connection details
db_name = "your_database_name"
db_user = "your_database_user"
db_password = "your_database_password"
db_host = "your_database_host"
db_port = "your_database_port"

# Provider API details
provider_url = "https://api.provider.com/transaction"
provider_headers = {
    "Authorization": "Bearer your_provider_token",
    "Content-Type": "application/json"
}

def fetch_data():
    try:
        response = requests.get(provider_url, headers=provider_headers)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as err:
        logging.error(f"Error fetching data: {err}")
        return None

def store_snapshot(data):
    conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
    cur = conn.cursor()

    for account in data['accounts']:
        account_id = account['id']
        balance = account['balance']
        date = datetime.now().strftime('%Y-%m-%d')

        # Check if snapshot already exists for today
        cur.execute("SELECT * FROM rat_account_snapshot WHERE account_id = %s AND date = %s", (account_id, date))
        if cur.fetchone() is None:
            cur.execute("INSERT INTO rat_account_snapshot (account_id, balance, date) VALUES (%s, %s, %s)", (account_id, balance, date))

    conn.commit()
    cur.close()
    conn.close()

def main():
    data = fetch_data()
    if data is not None:
        store_snapshot(data)

if __name__ == "__main__":
    main()