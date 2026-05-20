import requests
import psycopg2
import logging
import schedule
import time
import smtplib
from email.message import EmailMessage

# Define the public APIs to ingest data from
public_sources = [
    'https://api.pcpartpicker.com/v1/components/',
    'https://api.amazon.com/items/',
    'https://api.newegg.com/items/'
]

# Define the PostgreSQL database connection parameters
db_host = 'localhost'
db_name = 'catalog'
db_user = 'axentx'
db_password = 'password'

# Define the email alert parameters
email_sender = 'axentx@example.com'
email_receiver = 'axentx@example.com'
email_password = 'password'

def ingest_data():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password
        )
        cur = conn.cursor()

        # Ingest data from each public source
        for source in public_sources:
            response = requests.get(source)
            data = response.json()

            # Store the fetched records in the PostgreSQL catalog table
            for record in data:
                cur.execute('INSERT INTO catalog (id, name, description) VALUES (%s, %s, %s)', (record['id'], record['name'], record['description']))

        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        # Log success
        logging.info('Data ingestion successful')

    except Exception as e:
        # Log failure and send an email alert
        logging.error('Data ingestion failed: ' + str(e))
        send_email_alert('Data Ingestion Failed', 'Data ingestion failed: ' + str(e))

def send_email_alert(subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_sender
    msg['To'] = email_receiver

    with smtplib.SMTP_SSL('smtp.example.com', 465) as smtp:
        smtp.login(email_sender, email_password)
        smtp.send_message(msg)

# Schedule the ingestion script to run every 24 hours
schedule.every(24).hours.do(ingest_data)

while True:
    schedule.run_pending()
    time.sleep(1)