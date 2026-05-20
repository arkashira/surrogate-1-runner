from django.urls import path
from .views import get_template, save_template

urlpatterns = [
    path('api/templates/<str:template_id>/', get_template, name='get_template'),
    path('api/templates/<str:template_id>/', save_template, name='save_template'),
]