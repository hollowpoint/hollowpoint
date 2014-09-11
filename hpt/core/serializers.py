from .models import TaskState
from rest_framework import serializers

class TaskStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskState
