from django.contrib.auth.models import User

from rest_framework import serializers
from data_app.models import Contact, Category, Task


######################CONTACT######################


class ContactSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )

    class Meta:
        model = Contact
        fields = ["url", "user_id", "name", "email", "phone", "color"]


class ContactHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )

    class Meta:
        model = Contact
        fields = ["id", "user_id", "name", "email", "phone", "color"]


######################CATEGORY######################


class CategorySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user"
    )

    class Meta:
        model = Category
        fields = ["id", "user_id", "name", "color"]


######################TASKS######################


class TaskSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    contacts = serializers.SerializerMethodField()
    # contacts = "test"

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "category",
            "contacts",
            "due_date",
            "priority",
            "process_step",
        ]

    def create(self, validated_data):
        category_data = validated_data.pop("category")
        category, _ = Category.objects.get_or_create(
            user=self.context["request"].user,
            name=category_data["name"],
            defaults={"color": category_data["color"]},
        )
        validated_data["category"] = category
        return super().create(validated_data)

    def get_category(self, obj):
        """
        Entfernt 'user_id' aus der Kategorie-Darstellung in Tasks.
        """
        category_data = CategorySerializer(obj.category).data
        category_data.pop("user_id", None)  # Entfernt user_id, falls vorhanden
        return category_data

    def get_contacts(self, obj):
        """
        Entfernt 'user_id' aus der Kontakte-Darstellung in Tasks.
        """
        contacts_data = ContactSerializer(
            obj.contacts.all(),
            many=True,
            context=self.context,  # Hier self.context verwenden
        ).data
        for contact in contacts_data:
            contact.pop("user_id", None)  # Entfernt user_id aus jedem Kontakt
        return contacts_data


# class ContactHyperlinkedSerializer(serializers.HyperlinkedModelSerializer):
#    user_id = serializers.PrimaryKeyRelatedField(
#        queryset=User.objects.all(), source="user"
#    )
#
#    class Meta:
#        model = Contact
#        fields = ["id", "user_id", "name", "email", "phone", "color"]
