from rest_framework import serializers
from tasks.models import TaskModel
from django.utils import timezone
from accounts.models import User


class TaskModelSerializer(serializers.ModelSerializer):
    """serializer class"""

    class Meta:
        model = TaskModel
        fields = ['id', 'user', 'title', 'description', 'due_date', 'status', 'assigned_users', 'created', 'updated']


class TaskModelCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskModel
        fields = ['user', 'title', 'description', 'due_date', 'status', 'assigned_users']

    def validate_due_date(self, value):
        """Validate that the due date is in the future."""
        if value <= timezone.now():
            raise serializers.ValidationError("The due date must be in the future.")
        return value

    def validate_user(self, value):
        """Validate that the user is the authenticated user."""
        request_user = self.context['request'].user
        if value != request_user:
            raise serializers.ValidationError("You can only create tasks for yourself.")
        return value

    def create(self, validated_data):
        """Custom create method to save the task and handle ManyToMany assignment."""
        # Pop 'assigned_users' from validated_data
        assigned_users = validated_data.pop('assigned_users', [])

        # Create the task without the assigned users
        task = TaskModel.objects.create(**validated_data)

        # Now assign the users to the ManyToMany field
        if assigned_users:
            task.assigned_users.set(assigned_users)

        return task

    def save(self, **kwargs):
        """Custom save method to handle any additional logic."""
        task = self.create(self.validated_data)
        return task


