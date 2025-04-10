from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.db import models


from users_auth_app.models import User
from utils import generate_random_color, validate_hex_color


class Contact(models.Model):
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^[0-9+\-\(\)\/\s]*$",
                message="Enter a valid phone number. Only numbers, spaces, and the symbols +, -, /, and () are allowed.",
            )
        ],
        blank=True,
    )
    color = models.CharField(
        max_length=7, default=generate_random_color, validators=[validate_hex_color]
    )

    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contacts"
    )

    class Meta:
        unique_together = ("email", "created_by")

    def save(self, *args, **kwargs):
        """
        Splits the `name` field into `first_name` and `last_name` before saving the object.
        """
        name_parts = self.name.strip().split()
        self.first_name = name_parts[0] if name_parts else ""
        self.last_name = name_parts[1] if len(name_parts) > 1 else ""

        super().save(*args, **kwargs)
