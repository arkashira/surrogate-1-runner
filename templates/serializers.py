"""
Serializers for Template and TemplateVersion models.
"""

from rest_framework import serializers
from .models import Template, TemplateVersion


class TemplateVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateVersion
        fields = [
            "id",
            "template",
            "version_number",
            "content",
            "created_at",
            "created_by",
        ]


class TemplateSerializer(serializers.ModelSerializer):
    # Accept content on write, but never expose it on read
    content = serializers.JSONField(write_only=True)

    class Meta:
        model = Template
        fields = [
            "id",
            "name",
            "description",
            "content",
            "created_at",
            "updated_at",
            "latest_version",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "latest_version"]