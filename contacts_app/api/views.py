from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User


# Create your views here.


class ContactViewSet(ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Contact.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """
        Updates a contact if data has changed. Checks for duplicate names or emails.
        - Skips update if no changes are detected.
        - Raises validation errors if the new name or email already exists.
        - Updates user's email and username if changed.
        """
        contact = self.get_object()
        user = self.request.user
        data = serializer.validated_data

        new_name = data.get("name", contact.name)
        new_email = data.get("email", contact.email)
        new_phone_number = data.get("phone_number", contact.phone_number)

        unchanged = (
            contact.name == new_name and
            contact.email.lower() == new_email.lower() and
            contact.phone_number == new_phone_number
        )
        if unchanged:
            return

        if new_name.lower() != contact.name.lower():
            if Contact.objects.filter(name__iexact=new_name, created_by=user).exclude(pk=contact.pk).exists():
                raise ValidationError({"name": "A contact with this name already exists."})

        if new_email.lower() != contact.email.lower():
            if User.objects.filter(email__iexact=new_email).exclude(pk=user.pk).exists():
                raise ValidationError({"email": "A user with that email already exists."})
            user.email = new_email

        user.username = new_name
        user.save()
        serializer.save()
