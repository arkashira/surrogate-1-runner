from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime

app = Flask(__name__)

class FeedbackForm:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.message = ""

    def validate(self):
        return self.name and self.email and self.message

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = FeedbackForm()
    if request.method == 'POST':
        form.name = request.form['name']
        form.email = request.form['email']
        form.message = request.form['message']
        
        if form.validate():
            # Save the feedback to a database or send an email
            print(f"Feedback received at {datetime.now()}: {form.name} <{form.email}> said: {form.message}")
            return redirect(url_for('thank_you'))
    
    return render_template('form.html', form=form)

@app.route('/thank-you')
def thank_you():
    return "Thank you for your feedback!"

if __name__ == '__main__':
    app.run(debug=True)