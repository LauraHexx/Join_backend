from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets


from utils import generate_random_color
from tasks_app.models import Task, Subtask, Category
from tasks_app.api.serializers import (
    TaskSerializer,
    SubtaskSerializer,
    CategorySerializer,
    SummarySerializer,
)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)


class SubtaskViewSet(ModelViewSet):
    serializer_class = SubtaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subtask.objects.filter(task__created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Ensures the user is allowed to add subtasks to the task and saves the subtask.
        """
        task = serializer.validated_data.get("task")
        if task.created_by != self.request.user:
            raise serializers.ValidationError(
                {"task": "You do not have permission to add subtasks to this task."}
            )
        serializer.save()

    def perform_update(self, serializer):
        """
        Ensures the user is allowed to assign a subtask to the specified task and saves the subtask.
        """
        task = serializer.validated_data.get("task", serializer.instance.task)
        if task.created_by != self.request.user:
            raise serializers.ValidationError(
                {
                    "task": "You do not have permission to assign this subtask to the specified task."
                }
            )
        serializer.save()


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """
        Generates a random color if not provided and saves the object with the current user as the creator.
        """
        color = serializer.validated_data.get("color", None)

        if not color:
            color = generate_random_color()

        serializer.save(created_by=self.request.user)


class SummaryViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = SummarySerializer(instance={}, context={"request": request})
        return Response(serializer.data)
