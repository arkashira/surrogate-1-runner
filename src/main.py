from src.email_sender import EmailSender
from src.data_fetcher import DataFetcher
import schedule
import time

def send_daily_emails():
    data_fetcher = DataFetcher()
    email_sender = EmailSender("smtp.example.com", 587, "sender@example.com", "password")

    users = data_fetcher.get_users_with_accounts()
    for user in users:
        total_balance, mom_change = data_fetcher.get_account_summary(user['user_id'])
        email_sender.send_email(user['email'], user['name'], total_balance, mom_change)

def main():
    schedule.every().day.at("06:00").do(send_daily_emails)

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    main()