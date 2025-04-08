from django.contrib.auth.models import User

from rest_framework import serializers
from boards_app.models import Board


class BoardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Board
        fields = ["created_by"]
