from django.contrib.auth.models import User

from rest_framework import serializers
from data_app.models import Contact, Category, Task, Subtask
from django.utils.timezone import now


######################CONTACT######################


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ["url", "user", "name", "email", "phone", "color"]
        read_only_fields = ["user"]


######################CATEGORY######################


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["user", "id", "name", "color"]
        read_only_fields = ["user"]


######################SUBTASKS######################


class SubTaskReadSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="task.user", write_only=False
    )

    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), source="task.user", write_only=False
    )

    class Meta:
        model = Subtask
        fields = ["user_id", "task_id", "id", "name", "status"]


class SubTaskWriteSerializer(serializers.ModelSerializer):
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.none())

    class Meta:
        model = Subtask
        fields = ["task", "name", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user
        self.fields["task"].queryset = Task.objects.filter(user=user)


#######################SUMMARY######################


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
        read_only_fields = ["user"]

    def get_filtered_tasks(self, obj):
        return Task.objects.filter(user=obj["user"])

    def get_tasks_in_board(self, obj):
        tasks = self.get_filtered_tasks(obj)
        return tasks.count()

    def get_tasks_in_progress(self, obj):
        tasks = self.get_filtered_tasks(obj)
        return tasks.filter(process_step="inProgress").count()

    def get_tasks_awaiting_feedback(self, obj):
        tasks = self.get_filtered_tasks(obj)
        return tasks.filter(process_step="awaitingFeedback").count()

    def get_urgent_tasks(self, obj):
        tasks = self.get_filtered_tasks(obj)
        return tasks.filter(priority="urgent").count()

    def get_todo_tasks(self, obj):
        tasks = self.get_filtered_tasks(obj)
        return tasks.filter(process_step="todo").count()

    def get_done_tasks(self, obj):
        tasks = self.get_filtered_tasks(obj)
        return tasks.filter(process_step="done").count()

    def get_upcoming_deadline(self, obj):
        task = (
            self.get_filtered_tasks(obj)
            .exclude(due_date__lt=now().date())
            .order_by("due_date")
            .first()
        )
        return task.due_date if task else "No deadline"


######################TASKS######################
class TaskCategorySerializer(serializers.ModelSerializer):
    """Kategorie-Serializer für Tasks ohne user"""

    class Meta:
        model = Category
        fields = ["id", "name", "color"]


class TaskContactSerializer(serializers.ModelSerializer):
    """Kontakt-Serializer für Tasks ohne user"""

    class Meta:
        model = Contact
        fields = ["id", "name", "email", "phone", "color"]


class TaskSubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ["id", "name", "status"]


class TaskReadSerializer(serializers.ModelSerializer):
    category = TaskCategorySerializer(read_only=True)
    contacts = TaskContactSerializer(many=True, read_only=True)
    subtasks = TaskSubtaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
            "user_id",
            "id",
            "title",
            "description",
            "category",
            "contacts",
            "due_date",
            "priority",
            "process_step",
            "subtasks",
        ]


class TaskWriteSerializer(serializers.ModelSerializer):
    subtasks = TaskSubtaskSerializer(many=True, required=False)
    contacts = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Contact.objects.all()
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context["request"].user

        # Filter auf user-eigene Kontakte & Kategorien setzen
        self.fields["contacts"].queryset = Contact.objects.filter(user=user)
        self.fields["category"].queryset = Category.objects.filter(user=user)

    def validate_contacts(self, contacts):
        user = self.context["request"].user
        allowed_contacts = set(Contact.objects.filter(user=user))

        # Validierung vereinfacht
        invalid_contacts = [
            contact for contact in contacts if contact not in allowed_contacts
        ]
        if invalid_contacts:
            raise serializers.ValidationError(
                f"Contacts {[contact.id for contact in invalid_contacts]} are not allowed for this user."
            )

        return contacts

    def manage_contacts_and_subtasks(self, task, contacts_data, subtasks_data):
        """Setzt die Kontakte und Subtasks für das Task-Objekt."""
        if contacts_data is not None:
            task.contacts.set(contacts_data)

        if subtasks_data is not None:
            Subtask.objects.bulk_create(
                [Subtask(task=task, **subtask_data) for subtask_data in subtasks_data]
            )

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks", [])
        contacts = validated_data.pop("contacts", [])

        task = Task.objects.create(**validated_data)
        self.manage_contacts_and_subtasks(task, contacts, subtasks_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop("subtasks", None)
        contacts = validated_data.pop("contacts", None)

        # Alle anderen Attribute des Tasks aktualisieren
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Kontakte und Subtasks aktualisieren
        self.manage_contacts_and_subtasks(instance, contacts, subtasks_data)

        return instance
