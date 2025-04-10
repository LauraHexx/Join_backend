from django.db import models
from contacts_app.models import Contact
from users_auth_app.models import User
from utils import generate_random_color, validate_hex_color


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("urgent", "Urgent"),
        ("medium", "Medium"),
        ("low", "Low"),
    ]

    PROCESS_STEP_CHOICES = [
        ("todo", "To Do"),
        ("inProgress", "In Progress"),
        ("awaitingFeedback", "Awaiting Feedback"),
        ("done", "Done"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=30, choices=PRIORITY_CHOICES, default="medium"
    )
    contacts = models.ManyToManyField(Contact, related_name="tasks", blank=True)
    category = models.ForeignKey(
        "Category", on_delete=models.CASCADE, related_name="tasks"
    )

    process_step = models.CharField(
        max_length=20,
        choices=PROCESS_STEP_CHOICES,
        default="todo",
    )

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")


class Subtask(models.Model):
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
    task = models.ForeignKey("Task", on_delete=models.CASCADE, related_name="subtasks")


class Category(models.Model):
    name = models.CharField(max_length=30)
    color = models.CharField(
        max_length=7, default=generate_random_color, validators=[validate_hex_color]
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        unique_together = ("name", "created_by")
