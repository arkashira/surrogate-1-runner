from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Document, MentionNotification

User = get_user_model()


class DocumentEditSerializer(serializers.Serializer):
    """
    Validates the payload of an edit message.
    """
    content = serializers.CharField()
    cursor = serializers.DictField(
        child=serializers.IntegerField(),  # expects {"line": int, "ch": int}
        required=True,
    )
    document_id = serializers.IntegerField()

    def validate_document_id(self, value):
        if not Document.objects.filter(id=value).exists():
            raise serializers.ValidationError("Document does not exist.")
        return value


class MentionNotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for in‑app mention notifications.
    """
    mentioned_user_id = serializers.PrimaryKeyRelatedField(
        source="mentioned_user", queryset=User.objects.all()
    )
    document_id = serializers.PrimaryKeyRelatedField(
        source="document", queryset=Document.objects.all()
    )

    class Meta:
        model = MentionNotification
        fields = ("mentioned_user_id", "document_id", "message")