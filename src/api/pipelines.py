from flask import Blueprint, jsonify
from datetime import datetime

api = Blueprint('pipelines', __name__)

class Pipeline:
    def __init__(self, name, last_run_time, status):
        self.name = name
        self.last_run_time = last_run_time
        self.status = status

    @property
    def status_color(self):
        if self.status == 'Success':
            return 'green'
        elif self.status == 'Failed':
            return 'red'
        else:
            return 'blue'

def get_pipelines():
    # Dummy data for demonstration purposes
    pipelines = [
        Pipeline("Pipeline 1", datetime.now(), "Running"),
        Pipeline("Pipeline 2", datetime.now(), "Success"),
        Pipeline("Pipeline 3", datetime.now(), "Failed")
    ]
    return pipelines

@api.route('/api/pipelines', methods=['GET'])
def pipelines():
    pipelines = get_pipelines()
    response = []
    for pipeline in pipelines:
        response.append({
            'name': pipeline.name,
            'last_run_time': pipeline.last_run_time.isoformat(),
            'status': pipeline.status,
            'status_color': pipeline.status_color
        })
    return jsonify(response)