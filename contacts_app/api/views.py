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

    def perform_update(self, serializer):
        """
        Updates the user's email if the contact belongs to them and the new email is not already used.
        """
        contact = serializer.save()
        user = self.request.user
        new_email = contact.email.lower()
        old_email = user.email.lower()

        if contact.created_by == user and new_email != old_email:
            if (
                User.objects.filter(email__iexact=new_email)
                .exclude(pk=user.pk)
                .exists()
            ):
                raise ValidationError(
                    {"email": "A user with that username already exists"}
                )
            user.email = new_email
            user.save()
