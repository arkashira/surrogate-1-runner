from flask import Blueprint, request, jsonify
from src.models.compliance_result import ComplianceResult
from src.scanners.compliance_scanner import ComplianceScanner
from celery import chain
import uuid

compliance_api = Blueprint('compliance_api', __name__)

@compliance_api.route('/scan', methods=['POST'])
def start_compliance_scan():
    try:
        app_id = request.json.get('app_id')
        if not app_id:
            return jsonify({"error": "Missing app_id"}), 400

        scan_id = str(uuid.uuid4())
        result = ComplianceResult(
            scan_id=scan_id,
            status="queued",
            results={},
            app_id=app_id
        )
        result.save()

        # Chain: scan execution -> status update
        chain(
            ComplianceScanner().scan.s(scan_id, app_id),
            update_scan_status.s(scan_id)
        ).delay()

        return jsonify({
            "scan_id": scan_id,
            "status": "queued",
            "message": "Scan started"
        }), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def update_scan_status(scan_id, result):
    scan_result = ComplianceResult.get_by_id(scan_id)
    if scan_result:
        scan_result.status = "completed"
        scan_result.results = result
        scan_result.save()
    return result