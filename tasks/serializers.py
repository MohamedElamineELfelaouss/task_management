from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "due_date", "priority", "status"]
        read_only_fields = ["id", "status"]  # Optional: Fields the user cannot modify
