from flask import Flask, render_template, request
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('templates.html', active_page='home')

@app.route('/hardware')
def hardware():
    return render_template('templates.html', active_page='hardware')

@app.route('/games')
def games():
    return render_template('templates.html', active_page='games')

@app.route('/community')
def community():
    return render_template('templates.html', active_page='community')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))