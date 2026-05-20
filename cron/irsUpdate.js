import axios
import json
import psycopg2
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# Configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "postgres",
    "password": "password",
    "database": "axentx",
    "port": 5432
}

EMAIL_CONFIG = {
    "host": "smtp.example.com",
    "port": 587,
    "secure": False,
    "auth": {
        "user": "admin@axentx.com",
        "pass": "email_password"
    },
    "from": "admin@axentx.com",
    "to": "admin@axentx.com"
}

IRS_API = "https://api.irs.gov/v2/rules/latest"

def fetch_irs_rules():
    try:
        response = axios.get(IRS_API)
        response.raise_for_status()
        return response.json()
    except axios.exceptions.RequestException as e:
        print(f"Error fetching IRS rules: {e}")
        raise

def get_stored_rules():
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT rules_json FROM irs_rules ORDER BY updated_at DESC LIMIT 1")
        result = cursor.fetchone()
        return json.loads(result[0]) if result else None
    except (psycopg2.Error, Exception) as e:
        print(f"Database error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def update_rules(new_rules):
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO irs_rules (rules_json, updated_at) VALUES (%s, NOW()) "
            "ON CONFLICT (updated_at) DO UPDATE SET rules_json = EXCLUDED.rules_json",
            (json.dumps(new_rules),)
        )
        conn.commit()
    except (psycopg2.Error, Exception) as e:
        print(f"Database update error: {e}")
        raise
    finally:
        if conn:
            conn.close()

def send_notification(old_rules, new_rules):
    msg = MIMEText(f"IRS Rules Updated. Old: {json.dumps(old_rules)} New: {json.dumps(new_rules)}")
    msg['Subject'] = "IRS Rules Update Notification"
    msg['From'] = EMAIL_CONFIG['from']
    msg['To'] = EMAIL_CONFIG['to']
    
    try:
        with smtplib.SMTP(EMAIL_CONFIG['host'], EMAIL_CONFIG['port']) as server:
            server.starttls()
            server.login(EMAIL_CONFIG['auth']['user'], EMAIL_CONFIG['auth']['pass'])
            server.send_message(msg)
        print("Notification email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

def main():
    print(f"Starting IRS rule update at {datetime.now()}")
    
    try:
        latest_rules = fetch_irs_rules()
        stored_rules = get_stored_rules()
        
        if json.dumps(latest_rules) != json.dumps(stored_rules):
            print("Rules have changed. Updating database and sending notification.")
            update_rules(latest_rules)
            send_notification(stored_rules, latest_rules)
        else:
            print("Rules are up to date.")
            
    except Exception as e:
        print(f"Error in IRS update job: {e}")
    finally:
        print("Update job completed.")

if __name__ == "__main__":
    main()