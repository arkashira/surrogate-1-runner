from flask import Blueprint, request, jsonify, abort
from . import db
from .models import Tip, TipFeedback
import random

api_bp = Blueprint("api", __name__)

# ---------- Tip generator ----------
@api_bp.route("/generate", methods=["GET"])
def generate_tip():
    user_id = request.args.get("user_id")
    if not user_id:
        abort(400, description="User ID is required")

    tips = Tip.query.all()
    if not tips:
        abort(404, description="No tips available")

    tip = random.choice(tips)
    return jsonify(
        tip_id=tip.id,
        content=tip.content,
        category=tip.category,
    )

# ---------- Feedback ----------
@api_bp.route("/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    tip_id = data.get("tipId") or data.get("tip_id")
    user_id = data.get("user_id")
    feedback = data.get("feedback")

    if not all([tip_id, user_id, feedback]):
        abort(400, description="Missing required fields")

    if feedback not in ("helpful", "irrelevant"):
        abort(400, description="Invalid feedback value")

    # Ensure tip exists
    tip = Tip.query.get(tip_id)
    if not tip:
        abort(404, description="Tip not found")

    fb = TipFeedback(tip_id=tip.id, user_id=user_id, feedback=feedback)
    db.session.add(fb)
    db.session.commit()

    return jsonify({"message": "Feedback recorded"}), 201