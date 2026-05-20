from flask import Flask, request, redirect, url_for

app = Flask(__name__)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    name = request.form['name']
    email = request.form['email']
    feedback = request.form['feedback']
    
    # Store feedback logic here (e.g., database insertion)
    store_feedback(name, email, feedback)
    
    return redirect(url_for('thank_you'))

def store_feedback(name, email, feedback):
    # Placeholder for storing feedback
    print(f"Feedback received from {name} ({email}): {feedback}")

@app.route('/thank_you')
def thank_you():
    return "Thank you for your feedback!"

if __name__ == '__main__':
    app.run(debug=True)