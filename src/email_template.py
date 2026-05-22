from jinja2 import Template

class EmailTemplate:
    def __init__(self):
        self.template = Template("""
        <html>
            <body>
                <h1>Account Growth Summary</h1>
                <p>Hello {{ user_name }},</p>
                <p>Here is your daily summary of account growth:</p>
                <ul>
                    <li>Total Balance: {{ total_balance }}</li>
                    <li>Month-over-Month Change: {{ mom_change }}%</li>
                </ul>
                <p>Best regards,<br>Axentx Team</p>
            </body>
        </html>
        """)

    def render(self, user_name, total_balance, mom_change):
        return self.template.render(
            user_name=user_name,
            total_balance=total_balance,
            mom_change=mom_change
        )