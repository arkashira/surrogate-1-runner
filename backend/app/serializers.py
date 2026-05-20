from rest_framework import serializers
from .models import RecordingJob

class RecordingJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordingJob
        fields = ['id', 'url', 'start_time', 'end_time', 'status']