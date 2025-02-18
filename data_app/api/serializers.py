from django.contrib.auth.models import User

from rest_framework import serializers
from data_app.models import Contact, Category


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
