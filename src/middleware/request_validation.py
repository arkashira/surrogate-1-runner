from flask import request, jsonify
from functools import wraps

def validate_component_filters(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        brand = request.args.get('brand')
        min_price = request.args.get('min_price')
        max_price = request.args.get('max_price')
        min_benchmark = request.args.get('min_benchmark')

        if brand and not isinstance(brand, str):
            return jsonify({'error': 'Brand must be a string'}), 400

        if min_price:
            try:
                min_price = float(min_price)
                if min_price < 0:
                    return jsonify({'error': 'Minimum price must be a positive number'}), 400
            except ValueError:
                return jsonify({'error': 'Minimum price must be a number'}), 400

        if max_price:
            try:
                max_price = float(max_price)
                if max_price < 0:
                    return jsonify({'error': 'Maximum price must be a positive number'}), 400
            except ValueError:
                return jsonify({'error': 'Maximum price must be a number'}), 400

        if min_benchmark:
            try:
                min_benchmark = float(min_benchmark)
                if min_benchmark < 0:
                    return jsonify({'error': 'Minimum benchmark score must be a positive number'}), 400
            except ValueError:
                return jsonify({'error': 'Minimum benchmark score must be a number'}), 400

        if min_price and max_price and min_price > max_price:
            return jsonify({'error': 'Minimum price cannot be greater than maximum price'}), 400

        return f(*args, **kwargs)
    return decorated_function