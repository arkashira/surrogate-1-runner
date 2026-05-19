from flask import Flask, jsonify, render_template
from scripts.monitor import detect_game

app = Flask(__name__)

@app.route('/')
def dashboard():
    """Serve the main dashboard page."""
    return render_template('monitor.html')

@app.route('/api/monitor')
def monitor():
    """API endpoint returning current game detection status."""
    game_info = detect_game()
    return jsonify({
        'game': game_info
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)