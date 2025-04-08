from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


from utils import generate_random_color
from tasks_app.models import Task, Subtask, Category
from tasks_app.api.serializers import (
    TaskSerializer,
    SubtaskSerializer,
    CategorySerializer,
)

from tasks_app.api.utils import get_next_due_date, format_due_date


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        contacts_data = serializer.validated_data.pop("contact_ids", [])
        task = serializer.instance

        print(
            "Contact IDs (direkt aus request.data):",
            self.request.data.get("contact_ids", None),
        )

        serializer.save()

        if contacts_data:
            task.contacts.set(contacts_data)
        else:
            task.contacts.clear()

        task.save()

    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task_id = task.id
        task.delete()
        return Response({"id": task_id}, status=status.HTTP_200_OK)


class SubtaskViewSet(ModelViewSet):
    serializer_class = SubtaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Subtask.objects.filter(task__created_by=self.request.user)



class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.action == "list":
            standard_categories = Category.objects.filter(id__in=[1, 2])
            user_categories = Category.objects.filter(created_by=self.request.user)
            return (
                Category.objects.filter(id__in=standard_categories.values("id"))
                | user_categories
            )
        else:
            return Category.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        color = serializer.validated_data.get("color", None)

        if not color:
            color = generate_random_color()

        serializer.save(created_by=self.request.user)

    def destroy(self, request, *args, **kwargs):
        category_id = kwargs.get("pk")

        try:
            category = Category.objects.get(id=category_id, created_by=request.user)
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND
            )

        category.delete()
        return Response({"id": category_id}, status=status.HTTP_200_OK)
