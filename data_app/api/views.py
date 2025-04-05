from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from data_app.models import Contact, Category, Task, Subtask
from .serializers import (
    ContactSerializer,
    ContactHyperlinkedSerializer,
    CategorySerializer,
    TaskReadSerializer,
    TaskWriteSerializer,
    SummarySerializer,
)
from user_auth_app.api.permissions import IsOwnerOrAdmin


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
class ContactViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()  # Für die automatische Bestimmung des `basename`


# nur lesen + hinfügen
class CategoryViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrAdmin]
    queryset = Task.objects.all()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TaskReadSerializer
        return TaskWriteSerializer


# nur lesen
class SummaryViewSet(viewsets.ViewSet):
    def list(self, request):
        summary_data = SummarySerializer(instance={}).data
        return Response(summary_data)
