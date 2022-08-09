from rest_framework import serializers
from task.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'deadline_date', 'status',
                  'priority', 'importance', 'created_date', 'updated_date', 'started_at', 'finished_at']
        read_only_fields = ['id', 'created_date', 'updated_date', 'started_at', 'finished_at']
