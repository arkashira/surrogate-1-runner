from flask import Blueprint, request, jsonify
from src.services.job_queue import JobQueue
from src.utils.validation import validate_hardening_payload

hardening_bp = Blueprint('hardening', __name__)
job_queue = JobQueue()

@hardening_bp.route('/windows', methods=['POST'])
def trigger_hardening():
    data = request.get_json()
    if not validate_hardening_payload(data):
        return jsonify({'error': 'Invalid payload'}), 400

    vm_ids = data.get('vm_ids')
    policy_version = data.get('policy_version', 'latest')

    job_id = job_queue.enqueue_hardening_job(vm_ids, policy_version)
    return jsonify({'job_id': job_id}), 202

@hardening_bp.route('/status/<job_id>', methods=['GET'])
def get_hardening_status(job_id):
    status = job_queue.get_job_status(job_id)
    if not status:
        return jsonify({'error': 'Job not found'}), 404

    return jsonify(status), 200