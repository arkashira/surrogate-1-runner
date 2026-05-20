from flask import Blueprint, request, jsonify
from src.middleware.request_validation import validate_component_filters

components_bp = Blueprint('components', __name__)

@components_bp.route('/api/components', methods=['GET'])
@validate_component_filters
def get_components():
    # Your existing code to fetch components based on query parameters
    pass