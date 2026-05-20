import pytest
from django.db import IntegrityError
from surrogate.models import FounderProfile

@pytest.mark.django_db
def test_founder_profile_creation():
    profile = FounderProfile.objects.create(
        email="test@example.com",
        password_hash="hashed_password",
        stage="idea",
        target_market="B2C",
        pricing_model="subscription",
        current_funnel="awareness",
        biggest_growth_pain="Acquisition"
    )
    assert profile.id is not None
    assert profile.email == "test@example.com"

@pytest.mark.django_db
def test_founder_profile_unique_email():
    FounderProfile.objects.create(
        email="test@example.com",
        password_hash="hashed_password"
    )
    with pytest.raises(IntegrityError):
        FounderProfile.objects.create(
            email="test@example.com",
            password_hash="hashed_password"
        )