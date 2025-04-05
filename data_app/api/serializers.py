from django.contrib.auth.models import User

from rest_framework import serializers
from data_app.models import Contact, Category, Task, Subtask
from django.utils.timezone import now


######################CONTACT######################


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ["url", "user", "name", "email", "phone", "color"]


class ContactHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "phone", "color"]


######################CATEGORY######################


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "user", "name", "color"]


######################SUBTASKS######################
class SubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ["id", "name", "status"]


######################TASKS######################
class TaskCategorySerializer(serializers.ModelSerializer):
    """Kategorie-Serializer für Tasks ohne user_id"""

    class Meta:
        model = Category
        fields = ["id", "name", "color"]


class TaskContactSerializer(serializers.ModelSerializer):
    """Kontakt-Serializer für Tasks ohne user_id"""

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "phone", "color"]


#
class alt(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, required=False)
    contacts = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), many=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "category",
            "contacts",
            "due_date",
            "priority",
            "process_step",
            "subtasks",
        ]

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks", [])
        contacts = validated_data.pop("contacts", [])

        task = Task.objects.create(**validated_data)
        task.contacts.set(contacts)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop("subtasks", None)
        contacts = validated_data.pop("contacts", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if contacts is not None:
            instance.contacts.set(contacts)

        if subtasks_data is not None:
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance


class SummarySerializer(serializers.Serializer):
    tasks_in_board = serializers.SerializerMethodField()
    tasks_in_progress = serializers.SerializerMethodField()
    tasks_awaiting_feedback = serializers.SerializerMethodField()
    urgent_tasks = serializers.SerializerMethodField()
    upcoming_deadline = serializers.SerializerMethodField()
    todo_tasks = serializers.SerializerMethodField()
    done_tasks = serializers.SerializerMethodField()

    class Meta:
        fields = [
            "tasks_in_board",
            "tasks_in_progress",
            "tasks_awaiting_feedback",
            "urgent_tasks",
            "upcoming_deadline",
            "todo_tasks",
            "done_tasks",
        ]

    def get_tasks_in_board(self, obj):
        return Task.objects.count()

    def get_tasks_in_progress(self, obj):
        return self._get_task_count(process_step="inProgress")

    def get_tasks_awaiting_feedback(self, obj):
        return self._get_task_count(process_step="awaitingFeedback")

    def get_urgent_tasks(self, obj):
        return self._get_task_count(priority="urgent")

    def get_upcoming_deadline(self, obj):
        task = (
            Task.objects.exclude(due_date__lt=now().date()).order_by("due_date").first()
        )
        return task.due_date if task else "No deadline"

    def get_todo_tasks(self, obj):
        return self._get_task_count(process_step="todo")

    def get_done_tasks(self, obj):
        return self._get_task_count(process_step="done")

    def _get_task_count(self, **filters):
        """
        Hilfsmethode, um die Anzahl der Tasks basierend auf Filtern zu berechnen.
        """
        return Task.objects.filter(**filters).count()


class TaskReadSerializer(serializers.ModelSerializer):
    category = TaskCategorySerializer(read_only=True)
    contacts = TaskContactSerializer(many=True, read_only=True)
    subtasks = SubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "category",
            "contacts",
            "due_date",
            "priority",
            "process_step",
            "subtasks",
        ]


1


class TaskWriteSerializer(serializers.ModelSerializer):
    subtasks = SubtaskSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "category",
            "contacts",
            "due_date",
            "priority",
            "process_step",
            "subtasks",
        ]

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks", [])
        contacts = validated_data.pop("contacts", [])

        task = Task.objects.create(**validated_data)
        task.contacts.set(contacts)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop("subtasks", None)
        contacts = validated_data.pop("contacts", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if contacts is not None:
            instance.contacts.set(contacts)

        if subtasks_data is not None:
            instance.subtasks.all().delete()
            for subtask_data in subtasks_data:
                Subtask.objects.create(task=instance, **subtask_data)

        return instance
