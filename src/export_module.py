
import csv
import json
import pdfkit
from django.http import HttpResponse
from .models import DiskGeometry

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    writer.writerow(['Disk ID', 'Size', 'Interface', 'Rotation Speed'])
    for disk in DiskGeometry.objects.all().values_list('disk_id', 'size', 'interface', 'rotation_speed'):
        writer.writerow(disk)
    response['Content-Disposition'] = 'attachment; filename="disk_geometry.csv"'
    return response

def export_json(request):
    data = list(DiskGeometry.objects.all().values())
    return HttpResponse(json.dumps(data), content_type='application/json')

def export_pdf(request):
    html = '<html><body><table><tr><th>Disk ID</th><th>Size</th><th>Interface</th><th>Rotation Speed</th></tr>'
    for disk in DiskGeometry.objects.all():
        html += f'<tr><td>{disk.disk_id}</td><td>{disk.size}</td><td>{disk.interface}</td><td>{disk.rotation_speed}</td></tr>'
    html += '</table></body></html>'
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="disk_geometry.pdf"'
    return response