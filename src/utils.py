import json
import requests

def get_pipeline_status():
    response = requests.get('http://localhost:8000/pipelines')
    return json.loads(response.text)