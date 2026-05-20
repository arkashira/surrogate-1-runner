import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

class AlertingSystem:
    def __init__(self, smtp_server, smtp_port, smtp_user, smtp_password, template_dir):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def send_email_alert(self, recipient, subject, data):
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = recipient
        msg['Subject'] = subject

        template = self.env.get_template('email.html')
        body = template.render(data=data)

        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_user, self.smtp_password)
        text = msg.as_string()
        server.sendmail(self.smtp_user, recipient, text)
        server.quit()

    def send_in_app_notification(self, user_id, message):
        # Placeholder for in-app notification logic
        print(f"In-app notification sent to user {user_id}: {message}")

    def trigger_alert(self, recipient, subject, data, user_id):
        self.send_email_alert(recipient, subject, data)
        self.send_in_app_notification(user_id, f"{subject}: {data['summary']}")

# Example usage
if __name__ == "__main__":
    alert_system = AlertingSystem(
        smtp_server="smtp.example.com",
        smtp_port=587,
        smtp_user="alert@example.com",
        smtp_password="password",
        template_dir="/opt/axentx/surrogate-1/src/alerting/templates"
    )
    alert_system.trigger_alert(
        recipient="user@example.com",
        subject="Cost Anomaly Detected",
        data={"summary": "Unusual cost pattern detected", "details": "Detailed information..."},
        user_id="12345"
    )