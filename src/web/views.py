from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from axentx import settings

@require_http_methods(['GET'])
def pipeline_status(request):
    return HttpResponse(get_pipeline_status())