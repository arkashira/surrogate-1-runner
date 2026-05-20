from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    """
    Extends the built‑in UserCreationForm with an email field.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already in use.')
        return email

class ProfileForm(forms.ModelForm):
    """
    Handles creation / update of the Profile model.
    """
    class Meta:
        model = Profile
        fields = ('product_type', 'mrr', 'mau', 'marketing_channels')
        widgets = {
            'product_type': forms.TextInput(attrs={'placeholder': 'SaaS'}),
            'marketing_channels': forms.TextInput(attrs={'placeholder': 'Email, Social Media'}),
        }