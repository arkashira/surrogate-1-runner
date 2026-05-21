import logging
from typing import Dict

import yaml
from alerta import Alerta
from email.message import EmailMessage
import smtplib

logger = logging.getLogger(__name__)

class AlertDispatcher:
    def __init__(self, alerta_url: str, alerta_api_key: str):
        self.alerta = Alerta(url=alerta_url, api_key=alerta_api_key)

    def send_email(self, subject: str, body: str, to: str):
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = 'axentx-surrogate-1@axentx.com'
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('axentx-surrogate-1@axentx.com', 'password')
            smtp.send_message(msg)

    def send_alert(self, severity: str, environment: str, message: str):
        self.alerta.send(
            severity=severity,
            environment=environment,
            event='Surrogate-1 Alert',
            text=message
        )

def calculate_rolling_average(expenses: Dict[str, float]) -> float:
    return sum(expenses.values()) / len(expenses)

def check_deviation(average: float, current: float) -> bool:
    return current > average * 1.2

def main():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    alert_dispatcher = AlertDispatcher(
        alerta_url=config['alerta_url'],
        alerta_api_key=config['alerta_api_key']
    )

    # Simulate expenses data
    expenses = {
        '2022-01-01': 100.0,
        '2022-01-02': 120.0,
        '2022-01-03': 110.0
    }

    average = calculate_rolling_average(expenses)
    current = sum(expenses.values()) / len(expenses)

    if check_deviation(average, current):
        alert_dispatcher.send_alert(
            severity='critical',
            environment='production',
            message='Monthly expenses exceeded 120% of average'
        )
        alert_dispatcher.send_email(
            subject='Surrogate-1 Alert: Monthly expenses exceeded 120% of average',
            body='Please investigate',
            to='financial.manager@axentx.com'
        )

if __name__ == '__main__':
    main()