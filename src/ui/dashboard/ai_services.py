
from django.shortcuts import render
from .models import AIService

def ai_services(request):
    services = AIService.objects.all()
    context = {'services': services}
    return render(request, 'dashboard/ai_services.html', context)