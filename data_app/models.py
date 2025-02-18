from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    color = models.CharField(max_length=7)  # Hex Code

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    color = models.CharField(max_length=20)  # Auswahl aus festen Farben


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=False, blank=False
    )
    contacts = models.ManyToManyField(Contact, blank=True)
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10,
        choices=[("low", "Low"), ("medium", "Medium"), ("urgent", "Urgent")],
    )
    process_step = models.CharField(
        max_length=20,
        choices=[
            ("todo", "To Do"),
            ("inProgress", "In Progress"),
            ("done", "Done"),
            ("awaitingFeedback", "Awaiting Feedback"),
        ],
    )


class Subtask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="subtasks")
    name = models.CharField(max_length=255)
    status = models.BooleanField(default=False)
