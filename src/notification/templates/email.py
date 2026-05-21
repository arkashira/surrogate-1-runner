"""
Email template definitions for the surrogate-1 notification system.

Templates are simple string.Template based definitions that can be rendered
with a context dictionary.  The module provides a registry (`EMAIL_TEMPLATES`)
and a helper (`get_template`) for lookup.
"""

from __future__ import annotations

import dataclasses
import string
from typing import Dict


@dataclasses.dataclass(frozen=True)
class EmailTemplate:
    """
    Represents a single email template consisting of a subject and a body.
    Both fields are interpreted as ``string.Template`` strings.
    """

    subject: str
    body: str

    def render(self, context: Dict[str, str]) -> Dict[str, str]:
        """
        Render the template with the supplied ``context`` using safe substitution.

        Returns
        -------
        dict
            ``{'subject': <rendered subject>, 'body': <rendered body>}``
        """
        subject_tpl = string.Template(self.subject)
        body_tpl = string.Template(self.body)

        rendered_subject = subject_tpl.safe_substitute(context)
        rendered_body = body_tpl.safe_substitute(context)

        return {"subject": rendered_subject, "body": rendered_body}


# ---------------------------------------------------------------------------
# Default template registry
# ---------------------------------------------------------------------------

# NOTE: The placeholders used here must match the keys supplied by the
# notification manager when it calls ``render``.
EMAIL_TEMPLATES: Dict[str, EmailTemplate] = {
    "task_assigned": EmailTemplate(
        subject="Task Assigned: ${task_id}",
        body=(
            "Hello ${assignee_name},\n\n"
            "You have been assigned a new task.\n\n"
            "Task ID: ${task_id}\n"
            "Title: ${task_title}\n"
            "Description: ${task_description}\n"
            "Due Date: ${task_due_date}\n\n"
            "Please review the task at your earliest convenience.\n\n"
            "Best regards,\n"
            "Surrogate‑1 Notification Service"
        ),
    ),
    "task_status_changed": EmailTemplate(
        subject="Task ${task_id} Status Updated to ${new_status}",
        body=(
            "Hello ${assignee_name},\n\n"
            "The status of task **${task_id}** has changed.\n\n"
            "Title: ${task_title}\n"
            "New Status: ${new_status}\n"
            "Changed By: ${changed_by}\n"
            "Timestamp: ${timestamp}\n\n"
            "You can view the task details here: ${task_url}\n\n"
            "Best regards,\n"
            "Surrogate‑1 Notification Service"
        ),
    ),
    # Additional templates can be added here following the same pattern.
}


def get_template(name: str) -> EmailTemplate:
    """
    Retrieve a registered :class:`EmailTemplate` by name.

    Parameters
    ----------
    name: str
        The key of the template in ``EMAIL_TEMPLATES``.

    Returns
    -------
    EmailTemplate
        The requested template.

    Raises
    ------
    KeyError
        If the template name is not registered.
    """
    try:
        return EMAIL_TEMPLATES[name]
    except KeyError as exc:
        raise KeyError(f"Email template '{name}' is not defined.") from exc