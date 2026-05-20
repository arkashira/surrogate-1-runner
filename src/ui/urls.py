from django.urls import path
from .task_dashboard import TaskDashboard

urlpatterns = [
    path('dashboard/', TaskDashboard.as_view(), name='task_dashboard'),
    path('dashboard/<int:task_id>/edit/', TaskDashboard.as_view(), name='task_edit'),
]