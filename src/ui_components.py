from typing import List, Dict
import streamlit as st
from usage_tracker import UsageTracker

class UIComponents:
    def __init__(self, usage_tracker: UsageTracker):
        self.usage_tracker = usage_tracker

    def display_cloud_accounts(self, user_id: str):
        cloud_accounts = self.usage_tracker.get_cloud_accounts(user_id)
        st.subheader("Cloud Accounts")
        for account in cloud_accounts:
            st.write(f"- {account}")

        if len(cloud_accounts) >= 5:
            st.warning("You have reached the maximum number of cloud accounts (5) for the free tier. Please upgrade to add more.")

    def display_alerts(self, user_id: str):
        alerts = self.usage_tracker.get_alerts(user_id)
        st.subheader("Alerts")
        for alert in alerts:
            st.write(f"- {alert['timestamp']}: {alert['message']}")

    def display_upgrade_message(self):
        st.subheader("Upgrade to Pro")
        st.write("Unlock more cloud accounts and advanced features by upgrading to our Pro tier.")
        st.button("Upgrade Now")