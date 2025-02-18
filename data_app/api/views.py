from rest_framework import viewsets, mixins
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from data_app.models import Contact, Category, Task, Subtask
from .serializers import (
    ContactSerializer,
    ContactHyperlinkedSerializer,
    CategorySerializer,
    TaskSerializer,
)


# Create your views here.


# kann alles
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def list(self, request):
        serializer = ContactSerializer(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        contact = get_object_or_404(self.queryset, pk=pk)
        serializer = ContactHyperlinkedSerializer(contact, context={"request": request})
        return Response(serializer.data)


# nur lesen + hinfügen
class CategoryViewSet(mixins.CreateModelMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request):
        serializer = TaskSerializer(
            self.queryset, many=True, context={"request": request}
        )
        return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #    contact = get_object_or_404(self.queryset, pk=pk)
    #    serializer = ContactHyperlinkedSerializer(contact, context={"request": request})
    #    return Response(serializer.data)
