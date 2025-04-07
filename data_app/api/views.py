from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from data_app.models import Contact, Category, Task, Subtask
from .serializers import (
    ContactSerializer,
    CategorySerializer,
    TaskReadSerializer,
    TaskWriteSerializer,
    SubTaskReadSerializer,
    SubTaskWriteSerializer,
    SummarySerializer,
)
from user_auth_app.api.permissions import IsOwnerOrAdmin, IsSubtaskOwnerOrAdmin


# Create your views here.


class UserOwnedViewSet(viewsets.GenericViewSet):
    """
    Basisklasse für ViewSets, bei denen nur user-spezifische Daten angezeigt werden dürfen.
    """

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# kann alles
class ContactViewSet(UserOwnedViewSet, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


# nur lesen + hinfügen
class CategoryViewSet(
    UserOwnedViewSet, mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet
):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(UserOwnedViewSet, viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TaskReadSerializer
        return TaskWriteSerializer


class SubtaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsSubtaskOwnerOrAdmin]
    queryset = Subtask.objects.all()

    def get_queryset(self):
        # Zeige nur Subtasks, deren zugehöriger Task dem aktuellen User gehört
        return self.queryset.filter(task__user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SubTaskReadSerializer
        return SubTaskWriteSerializer


# nur lesen
class SummaryViewSet(UserOwnedViewSet, viewsets.ViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Task.objects.all()

    def list(self, request):
        summary_data = SummarySerializer(instance={"user": request.user}).data
        return Response(summary_data)
