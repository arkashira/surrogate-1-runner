
from django.template.loader import get_template
from django.http import JsonResponse

def disk_geometry_view(request):
    # ... ( existing code )

    # New: Check user agent for device type and adjust layout accordingly
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    is_mobile = 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent

    # New: Pass device type to the template for responsive layout
    template = get_template('disk_geometry.html')
    context = {
        'disk_data': disk_data,
        'is_mobile': is_mobile,
    }
    return JsonResponse(template.render(context, request))