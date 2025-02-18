from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from data_app.models import Contact
from .serializers import ContactSerializer, ContactHyperlinkedSerializer


# Create your views here.


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
