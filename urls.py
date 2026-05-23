from django.urls import path
from views.audit_log_view import AuditLogListView

urlpatterns = [
    path('api/audit', AuditLogListView.as_view(), name='audit-log-list'),
]