"""
Render functions for interactive components.
Return a string of HTML that will be inserted into the template.
"""

def render_feature_quiz():
    """A very small quiz about platform features."""
    return """
    <form method="post" action="/onboarding/quiz/submit">
        <p>Which of the following is NOT a core feature?</p>
        <label><input type="radio" name="answer" value="A"> A. Data Ingestion</label><br>
        <label><input type="radio" name="answer" value="B"> B. Model Training</label><br>
        <label><input type="radio" name="answer" value="C"> C. Email Marketing</label><br>
        <button type="submit">Submit</button>
    </form>
    """

INTERACTIVE_RENDERERS = {
    "feature_quiz": render_feature_quiz,
}