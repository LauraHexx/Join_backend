from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from ..models import Task, Subtask, Category
from contacts_app.models import Contact
from contacts_app.api.serializers import ContactSerializer


class SubtaskSerializer(serializers.ModelSerializer):
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), source="task", write_only=True, required=True
    )
    task = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subtask
        fields = ["id", "name", "status", "task", "task_id"]


class CategorySerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "color",
            "created_by",
        ]

    def validate_color(self, value):
        if not value.startswith("#") or len(value) != 7:
            raise serializers.ValidationError("Invalid color code")
        return value


class TaskSubtaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtask
        fields = ["name", "status"]


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    subtasks = TaskSubtaskSerializer(many=True)
    contacts = ContactSerializer(many=True, read_only=True)
    contact_ids = serializers.PrimaryKeyRelatedField(
        queryset=Contact.objects.all(), many=True, write_only=True
    )
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def validate_category_id(self, value):
        user = self.context["request"].user
        if not Category.objects.filter(id=value, created_by=user).exists():
            raise serializers.ValidationError(
                f"You do not have permission to use category with ID {value}."
            )
        return value

    def validate_contact_ids(self, value):
        user = self.context["request"].user
        invalid_contacts = []

        for contact in value:
            if contact.created_by != user:
                invalid_contacts.append(contact.id)

        if invalid_contacts:
            raise serializers.ValidationError(
                f"You do not have permission to use the following contact IDs: {', '.join(map(str, invalid_contacts))}."
            )

        return value

    def create(self, validated_data):
        subtasks_data = validated_data.pop("subtasks", [])
        contact_ids = validated_data.pop("contact_ids", [])
        category_id = validated_data.pop("category_id")
        user = self.context["request"].user

        category = get_object_or_404(Category, id=category_id, created_by=user)
        task = Task.objects.create(**validated_data, category=category, created_by=user)
        task.contacts.set(contact_ids)

        for subtask_data in subtasks_data:
            Subtask.objects.create(task=task, **subtask_data)

        return task

    def update(self, instance, validated_data):
        subtasks_data = validated_data.pop("subtasks", None)
        category_id = validated_data.pop("category_id", None)
        contact_ids = validated_data.pop("contact_ids", None)
        user = self.context["request"].user

        if category_id is not None:
            instance.category = get_object_or_404(
                Category, id=category_id, created_by=user
            )

        if contact_ids is not None:
            instance.contacts.set(contact_ids)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if subtasks_data is not None:
            existing_ids = [s.get("id") for s in subtasks_data if s.get("id")]

            instance.subtasks.exclude(id__in=existing_ids).delete()

            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get("id")
                if subtask_id:
                    subtask = get_object_or_404(Subtask, id=subtask_id, task=instance)
                    for key, value in subtask_data.items():
                        setattr(subtask, key, value)
                    subtask.save()
                else:
                    Subtask.objects.create(task=instance, **subtask_data)

        return instance
