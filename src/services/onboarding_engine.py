import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader

def send_onboarding_email(user, step):
    # Load the email template
    env = Environment(loader=FileSystemLoader('src/templates'))
    template = env.get_template('onboarding_step.html')
    
    # Render the email content
    email_content = template.render(user=user, step=step)

    # Setup the email parameters
    msg = MIMEMultipart()
    msg['From'] = 'noreply@axentx.com'
    msg['To'] = user.email
    msg['Subject'] = f'Onboarding Step: {step.title}'

    msg.attach(MIMEText(email_content, 'html'))

    # Send the email via SMTP
    with smtplib.SMTP('smtp.axentx.com', 587) as server:
        server.starttls()
        server.login('user', 'password')  # Replace with actual credentials
        server.send_message(msg)

def trigger_onboarding_step(user, step):
    # Trigger the onboarding step and send email
    # (Assuming some logic here to trigger the step)
    send_onboarding_email(user, step)