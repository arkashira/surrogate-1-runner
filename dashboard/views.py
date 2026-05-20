from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Alert

@login_required
def dashboard(request):
    """
    Displays all alerts on the dashboard.
    
    Args:
        request (HttpRequest): The current HTTP request.
    
    Returns:
        HttpResponse: The rendered dashboard template with alerts.
    """
    alerts = Alert.objects.all()
    return render(request, 'dashboard.html', {'alerts': alerts})