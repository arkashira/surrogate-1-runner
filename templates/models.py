"""
Django models for template storage with immutable versioning.
"""

from __future__ import annotations

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class Template(models.Model):
    """
    A reusable process template.  Only the latest version is stored on the
    ``latest_version`` FK; historic versions live in ``TemplateVersion``.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_templates",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Latest version pointer (nullable until first version is created)
    latest_version = models.ForeignKey(
        "TemplateVersion",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class TemplateVersion(models.Model):
    """
    Immutable snapshot of a template at a specific point in time.
    """
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name="versions",
    )
    version_number = models.PositiveIntegerField()
    content = models.JSONField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="template_versions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("template", "version_number")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.template.name} v{self.version_number}"


# --------------------------------------------------------------------------- #
# Helper functions – keep business logic out of the view layer.
# --------------------------------------------------------------------------- #
def get_latest_version(template: Template) -> TemplateVersion | None:
    """Return the latest version or ``None`` if no versions exist."""
    return template.latest_version


def create_template(name: str, content: dict, user: User, description: str = "") -> Template:
    """
    Create a new template and its first version atomically.
    """
    with models.transaction.atomic():
        template = Template.objects.create(
            name=name, description=description, created_by=user
        )
        version = TemplateVersion.objects.create(
            template=template,
            version_number=1,
            content=content,
            created_by=user,
        )
        template.latest_version = version
        template.save(update_fields=["latest_version"])
    return template


def update_template(template: Template, content: dict, user: User) -> TemplateVersion:
    """
    Append a new version to an existing template.
    """
    with models.transaction.atomic():
        last = template.versions.order_by("-version_number").first()
        new_number = (last.version_number + 1) if last else 1
        version = TemplateVersion.objects.create(
            template=template,
            version_number=new_number,
            content=content,
            created_by=user,
        )
        template.latest_version = version
        template.save(update_fields=["latest_version"])
    return version