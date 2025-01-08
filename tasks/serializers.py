from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Includes all fields for CRUD operations and read-only fields for managed attributes.
    """

    class Meta:
        model = Task
        fields = [
            "id",  # Global task ID
            "title",  # Task title
            "description",  # Task description
            "due_date",  # Task due date
            "priority",  # Priority level (Low, Medium, High)
            "status",  # Task status (Pending, Completed)
            "completed_at",  # Timestamp when the task was marked as complete
        ]
        read_only_fields = [
            "id",  # Global ID is managed by Django
            "user",  # The user is set by the backend logic
            "completed_at",  # Only updated when marking the task as complete
        ]


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Includes all fields necessary for user management and hashes passwords.
    """

    class Meta:
        model = User
        fields = [
            "id",  # User ID
            "username",  # Username
            "email",  # Email address
            "password",  # Password (write-only)
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
            "email": {"required": False},
        }

    def create(self, validated_data):
        """
        Hash the password before saving the user.
        """
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Handle updates, including hashing the password if provided.
        """
        if "password" in validated_data:
            instance.set_password(validated_data.pop("password"))
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("username", instance.username)
        instance.save()
        return instance


class TaskStatusUpdateSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=["complete", "incomplete"])
