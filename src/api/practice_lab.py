from flask import Blueprint, request, jsonify
from src.models.practice_lab import PracticeLab
from src.services.practice_lab_service import PracticeLabService

practice_lab_bp = Blueprint('practice_lab', __name__)

@practice_lab_bp.route('/practice_labs', methods=['GET'])
def get_practice_labs():
    objective = request.args.get('objective')
    difficulty = request.args.get('difficulty')
    practice_labs = PracticeLabService.get_practice_labs(objective, difficulty)
    return jsonify([lab.to_dict() for lab in practice_labs])

@practice_lab_bp.route('/practice_labs/<int:lab_id>', methods=['GET'])
def get_practice_lab(lab_id):
    practice_lab = PracticeLabService.get_practice_lab_by_id(lab_id)
    if practice_lab:
        return jsonify(practice_lab.to_dict())
    else:
        return jsonify({'error': 'Practice lab not found'}), 404