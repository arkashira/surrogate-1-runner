import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import os
from datetime import datetime

def send_playbook_notification(founder_id: int, playbook_url: str, email_address: str) -> bool:
    """
    Send notification email to founder with link to new playbook
    
    Args:
        founder_id: The ID of the founder
        playbook_url: URL to the generated playbook
        email_address: Email address of the founder
        
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    # Email configuration
    smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    
    if not all([sender_email, sender_password]):
        raise ValueError("Email credentials not configured")
    
    # Create message
    message = MIMEMultipart("alternative")
    message["Subject"] = f"Your Weekly Playbook is Ready - Foundry #{founder_id}"
    message["From"] = sender_email
    message["To"] = email_address
    
    # HTML content
    html_content = f"""
    <html>
      <body>
        <p>Hello,</p>
        
        <p>Your weekly playbook has been generated successfully!</p>
        
        <p><a href="{playbook_url}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">View Your Playbook</a></p>
        
        <p>This playbook contains actionable steps based on your profile and market insights.</p>
        
        <p>Best regards,<br>The Axentx Team</p>
      </body>
    </html>
    """
    
    # Plain text content
    text_content = f"""Hello,

Your weekly playbook has been generated successfully!

{playbook_url}

This playbook contains actionable steps based on your profile and market insights.

Best regards,
The Axentx Team"""
    
    # Add parts to message
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")
    
    message.attach(part1)
    message.attach(part2)
    
    try:
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        return True
        
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False