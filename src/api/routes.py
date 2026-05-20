from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import get_current_user, jwt_required
from models import User, Term, db

class TermsResource(Resource):
    @jwt_required()
    def post(self, term_id):
        """Mark a term as learned by the current user"""
        current_user = get_current_user()
        term = Term.query.get_or_404(term_id)
        
        if term in current_user.learned_terms:
            return jsonify({"msg": "Term already marked as learned", "term_id": term_id}), 200

        current_user.learned_terms.append(term)
        db.session.commit()
        return jsonify({"msg": "Term marked as learned", "term_id": term_id}), 201