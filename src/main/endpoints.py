from flask import Flask, jsonify
from emulator import Emulator

app = Flask(__name__)
emulator = Emulator()

@app.route('/status', methods=['GET'])
def get_status():
    status = emulator.get_status()
    return jsonify(status)

if __name__ == '__main__':
    app.run(debug=True)