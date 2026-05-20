from flask import Blueprint, jsonify, request
from .external_actions import get_external_actions

compliance_bp = Blueprint('compliance', __name__)

@compliance_bp.route('/dashboard', methods=['GET'])
def compliance_dashboard():
    # Fetch external actions and their SHAs
    external_actions = get_external_actions()
    
    # Apply filters and sorting based on query parameters
    filtered_sorted_actions = filter_and_sort_actions(external_actions, request.args)
    
    return jsonify(filtered_sorted_actions)

def filter_and_sort_actions(actions, query_params):
    # Implement filtering and sorting logic based on query parameters
    filtered_actions = []
    for action in actions:
        if matches_filter(action, query_params):
            filtered_actions.append(action)
    
    sorted_actions = sorted(filtered_actions, key=lambda x: x['sha'])
    return sorted_actions

def matches_filter(action, query_params):
    # Implement filter matching logic based on query parameters
    for param, value in query_params.items():
        if param in action and action[param] != value:
            return False
    return True