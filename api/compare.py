from flask import Flask, request, jsonify
from axentx.cpu_data import get_cpus, filter_cpus

app = Flask(__name__)

@app.route('/api/compare', methods=['GET'])
def compare_cpus():
    brand = request.args.get('brand', default=None, type=str)
    min_price = request.args.get('min_price', default=None, type=float)
    max_price = request.args.get('max_price', default=None, type=float)
    min_performance = request.args.get('min_performance', default=None, type=float)
    max_performance = request.args.get('max_performance', default=None, type=float)

    cpus = get_cpus()
    filtered_cpus = filter_cpus(cpus, brand=brand, min_price=min_price, max_price=max_price, min_performance=min_performance, max_performance=max_performance)

    return jsonify(filtered_cpus)

if __name__ == '__main__':
    app.run(debug=True)