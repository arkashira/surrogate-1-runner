from django.urls import path
from .views import questionnaire, success

urlpatterns = [
    path('questionnaire/', questionnaire, name='questionnaire'),
    path('success/', success, name='success'),
]