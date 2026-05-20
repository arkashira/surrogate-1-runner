
import smtplib
from email.message import EmailMessage
from django.conf import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.EMAIL_SMTP_SERVER
        self.smtp_port = settings.EMAIL_SMTP_PORT
        self.smtp_username = settings.EMAIL_SMTP_USERNAME
        self.smtp_password = settings.EMAIL_SMTP_PASSWORD
        self.sender_email = settings.EMAIL_SENDER

    def send_verification_email(self, recipient_email, verification_token):
        msg = EmailMessage()
        msg.set_content(f'Your verification token is: {verification_token}')
        msg['Subject'] = 'Verify your email'
        msg['From'] = self.sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)

# /opt/axentx/surrogate-1/backend/app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, null=True, blank=True)

# /opt/axentx/surrogate-1/backend/app/views.py

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .services.email import EmailService
import uuid

User = get_user_model()

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate password complexity
        if len(password) < 8 or not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            return JsonResponse({'error': 'Password must be at least 8 characters and contain a mix of letters and numbers'}, status=400)

        # Create user
        user = User.objects.create_user(email=email, password=password)
        verification_token = uuid.uuid4().hex
        user.verification_token = verification_token
        user.save()

        # Send verification email
        email_service = EmailService()
        email_service.send_verification_email(email, verification_token)

        return JsonResponse({'message': 'Registration successful. Please check your email for verification.'}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

# /opt/axentx/surrogate-1/backend/app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
]

## Summary
- Implemented email verification service using SMTP config
- Added is_verified and verification_token fields to CustomUser model
- Created registration view with email verification token generation and email sending
- Updated URL patterns to include registration endpoint