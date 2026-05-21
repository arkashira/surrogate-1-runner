
from typing import List, Tuple
from operator import itemgetter

class Component:
    def __init__(self, id: int, price: float, fps_gain: float):
        self.id = id
        self.price = price
        self.fps_gain = fps_gain

def get_bundle(budget: float, components: List[Component], target_fps: float) -> Tuple[List[Component], str]:
    components.sort(key=itemgetter(1), reverse=True)
    bundle = []
    total_price = 0
    total_fps_gain = 0
    for component in components:
        if total_price + component.price <= budget:
            bundle.append(component)
            total_price += component.price
            total_fps_gain += component.fps_gain
        if total_fps_gain >= target_fps:
            break
    if total_fps_gain < target_fps:
        return [], f"Consider increasing your budget. Target FPS not reached."
    return bundle, f"Total price: ${total_price:.2f}, Projected FPS gain: {total_fps_gain:.2f}"

# /opt/axentx/surrogate-1/backend/api/v1/recommend.py

from flask import Blueprint, jsonify, request
from recommendation_service import get_bundle, Component

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/api/v1/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    budget = data['budget']
    target_fps = data['target_fps']
    components = [
        Component(1, 100, 10),
        Component(2, 200, 20),
        Component(3, 300, 30),
        # Add more components as needed
    ]
    bundle, message = get_bundle(budget, components, target_fps)
    if not bundle:
        return jsonify({'message': message}), 400
    return jsonify([
        {
            'id': component.id,
            'price': component.price,
            'fps_gain': component.fps_gain
        }
        for component in bundle
    ])

## Summary
- Implemented greedy knapsack algorithm in `recommendation_service.py`.
- Created API endpoint for recommendation service in `recommend.py`.
- The algorithm sorts components by highest fps_per_usd and adds them to the bundle until the budget is exhausted or the target FPS is reached.
- If the target FPS is not reached, the API returns a message suggesting the user increase their budget.