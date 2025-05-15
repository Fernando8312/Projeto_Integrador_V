from rest_framework import serializers
from .models import Worker, AccessRecord

class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'name', 'tag_uid', 'max_exposure_minutes']

class AccessRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRecord
        fields = ['id', 'worker', 'entry_time', 'exit_time', 'exposure_duration']