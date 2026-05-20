import os
import smtplib
from datetime import datetime, timedelta
from app.models.budget_rules import BudgetRules
from app.utils.email_service import send_email

def check_budget_and_alert():
    budget_rules = BudgetRules.get_current_rules()
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)

    for budget in budget_rules:
        total_spend = budget.get_total_spend(one_week_ago, today)
        if total_spend >= (budget.budget * 0.8):
            days_left = (datetime(today.year, today.month + 1, 1) - today).days
            remaining_budget = budget.budget - total_spend
            forecast = remaining_budget / days_left
            alert_message = f"Your budget is {total_spend} out of {budget.budget}. You have {days_left} days left with a forecast of {forecast} per day."
            send_email(budget.user.email, "Budget Alert", alert_message)

# /opt/axentx/surrogate-1/app/models/budget_rules.py
from peewee import *

db = SqliteDatabase('budget.db')

class BaseModel(Model):
    class Meta:
        database = db

class BudgetRules(BaseModel):
    user = ForeignKeyField('User', backref='budget_rules')
    budget = DecimalField()
    currency = CharField()

    @classmethod
    def get_current_rules(cls):
        return cls.select()

    def get_total_spend(self, start_date, end_date):
        # Implement logic to get total spend between start_date and end_date
        pass