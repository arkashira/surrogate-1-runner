from flask import render_template
from models import Feedback

@app.route('/admin/feedback')
def view_feedback():
    feedbacks = Feedback.query.all()
    return render_template('feedback_list.html', feedbacks=feedbacks)