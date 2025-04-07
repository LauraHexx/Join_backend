from rest_framework import serializers
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    repeated_password = serializers.CharField(
        max_length=128, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "repeated_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Diese E-Mail-Adresse wird bereits verwendet."
            )
        return value

    def save(self):
        pw = self.validated_data["password"]
        repeated_pw = self.validated_data["repeated_password"]

        if pw != repeated_pw:
            raise serializers.ValidationError({"error": "passwords don't match"})

        account = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        account.set_password(pw)
        account.save()
        return account
