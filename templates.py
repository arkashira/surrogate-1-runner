from flask import Flask, render_template, request, redirect, url_for, flash
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory storage for templates
templates = []

def get_templates():
    return templates

def create_template(name, description):
    if any(t['name'] == name for t in templates):
        return None, "A template with this name already exists."
    new_template = {
        'id': str(uuid.uuid4()),
        'name': name,
        'description': description,
        'steps': []
    }
    templates.append(new_template)
    return new_template, None

@app.route('/templates', methods=['GET', 'POST'])
def templates_page():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        template, error = create_template(name, description)
        if error:
            flash(error)
        else:
            flash(f"Template '{name}' created successfully!")
            return redirect(url_for('templates_page'))
    return render_template('templates.html')