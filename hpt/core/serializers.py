from .models import TaskState, TaskMeta, WorkerState
from rest_framework import serializers


class TaskStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskState


class WorkerStateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WorkerState


class TaskMetaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaskMeta
