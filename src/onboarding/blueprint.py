import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from .steps import ONBOARDING_STEPS
from .renderers import INTERACTIVE_RENDERERS

bp = Blueprint(
    "onboarding",
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    url_prefix="/onboarding",
)

@bp.route("/")
def index():
    """Redirect to the first step."""
    return redirect(url_for("onboarding.step", step_id=1))

@bp.route("/step/<int:step_id>", methods=["GET", "POST"])
def step(step_id):
    """Render a specific onboarding step."""
    step = next((s for s in ONBOARDING_STEPS if s["id"] == step_id), None)
    if not step:
        return "Step not found", 404

    # Handle interactive form submissions
    if request.method == "POST" and step.get("interactive"):
        # For simplicity, just redirect to the next step after submission
        return redirect(url_for("onboarding.step", step_id=step_id + 1))

    interactive_html = ""
    if step.get("interactive"):
        renderer = INTERACTIVE_RENDERERS.get(step["interactive"])
        if renderer:
            interactive_html = renderer()

    return render_template(
        "interactive_guide.html",
        step=step,
        interactive_html=interactive_html,
        total_steps=len(ONBOARDING_STEPS),
        current_step=step_id,
    )

@bp.route("/quiz/submit", methods=["POST"])
def quiz_submit():
    """Handle quiz submission."""
    answer = request.form.get("answer")
    if answer == "C":
        feedback = "Correct! Email Marketing is not a core feature."
    else:
        feedback = "Incorrect. Try again."
    # Show feedback and let the user retry the same step
    flash(feedback)
    return redirect(url_for("onboarding.step", step_id=3))