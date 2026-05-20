from flask import Blueprint, jsonify
from .models.roth import get_roth_guide_steps

roth_api = Blueprint('roth_api', __name__)

@roth_api.route('/api/roth/guide', methods=['GET'])
def roth_guide():
    steps = get_roth_guide_steps()
    return jsonify(steps)