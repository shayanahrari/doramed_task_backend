from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from tasks.models import TaskModel
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from tasks import serializers
from rest_framework_tracking.mixins import LoggingMixin


class TaskListView(LoggingMixin, generics.ListAPIView):
    """task list view
    List all tasks
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.TaskModelSerializer

    def get_queryset(self):
        """Return tasks only for the authenticated user."""
        return TaskModel.objects.filter(user=self.request.user)


class TaskDetailView(LoggingMixin, generics.RetrieveAPIView):
    """task detail view
    Retrieve a specific task
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.TaskModelSerializer

    def get_queryset(self):
        """Return the task only if it belongs to the authenticated user."""
        return TaskModel.objects.filter(user=self.request.user)


class TaskUpdateView(LoggingMixin, generics.UpdateAPIView):
    """ task update view
    Update an existing task
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.TaskModelSerializer

    def get_queryset(self):
        """Return the task only if it belongs to the authenticated user."""
        return TaskModel.objects.filter(user=self.request.user)


class TaskDeleteView(LoggingMixin, generics.DestroyAPIView):
    """ task delete view
    Delete a task
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = serializers.TaskModelSerializer

    def get_queryset(self):
        """Return the task only if it belongs to the authenticated user."""
        return TaskModel.objects.filter(user=self.request.user)


class TaskCreateView(LoggingMixin, APIView):
    """handle creating task"""
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        ser_data = serializers.TaskModelCreateSerializer(data=request.data, context={'request': request})

        if ser_data.is_valid():
            task = ser_data.save()
            task_ser_data = serializers.TaskModelSerializer(instance=task)
            return Response(task_ser_data.data, status=status.HTTP_201_CREATED)

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)





