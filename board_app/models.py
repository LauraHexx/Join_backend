from django.db import models
from users_auth_app.models import User


class Board(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="boards", null=True, blank=True
    )
