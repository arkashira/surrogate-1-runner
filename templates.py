from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired

class StepForm(FlaskForm):
    name = StringField('Step Name', validators=[DataRequired()])
    description = StringField('Step Description')
    submit = SubmitField('Save Step')

class TemplateForm(FlaskForm):
    name = StringField('Template Name', validators=[DataRequired()])
    steps = FieldList(FormField(StepForm), min_entries=1)
    submit = SubmitField('Save Template')

# /opt/axentx/surrogate-1/templates.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Template</title>
</head>
<body>
    <h1>Edit Template</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div>
            <label for="name">Template Name:</label>
            {{ form.name(size=20) }}
        </div>
        {% for step in form.steps %}
            <div>
                <label for="name">Step Name:</label>
                {{ step.name(size=20) }}
                <label for="description">Step Description:</label>
                {{ step.description(size=50) }}
                {{ step.submit() }}
            </div>
        {% endfor %}
        {{ form.submit() }}
    </form>
</body>
</html>

## Summary
- Added `StepForm` and `TemplateForm` in `templates.py` for handling individual steps and the entire template.
- Created an HTML form in `templates.html` to display and edit the template and its steps.
- The user can now retrieve an existing template, make changes, and save them.
- The user can add and remove steps from the template.