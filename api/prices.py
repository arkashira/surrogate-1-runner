from flask import Blueprint, jsonify
from datetime import datetime
from ..models import Component, Price
from ..extensions import db

prices_bp = Blueprint('prices', __name__)

@prices_bp.route('/api/components/<int:component_id>/prices', methods=['GET'])
def get_component_prices(component_id):
    component = Component.query.get_or_404(component_id)
    prices = Price.query.filter_by(component_id=component_id).order_by(Price.timestamp.desc()).all()
    return jsonify([{
        'vendor': price.vendor,
        'price': price.price,
        'timestamp': price.timestamp.isoformat()
    } for price in prices])

@prices_bp.route('/api/components/<int:component_id>/price', methods=['GET'])
def get_component_current_price(component_id):
    component = Component.query.get_or_404(component_id)
    prices = Price.query.filter_by(component_id=component_id).order_by(Price.price.asc()).limit(1).all()
    if not prices:
        return jsonify({'error': 'No price data available'}), 404
    return jsonify({
        'component_id': component_id,
        'current_price': prices[0].price,
        'vendor': prices[0].vendor,
        'timestamp': prices[0].timestamp.isoformat()
    })

def add_price(component_id, vendor, price):
    new_price = Price(
        component_id=component_id,
        vendor=vendor,
        price=price,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_price)
    db.session.commit()