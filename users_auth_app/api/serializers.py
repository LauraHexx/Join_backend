from rest_framework import serializers
from users_auth_app.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from contacts_app.models import Contact


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]
        read_only_fields = ["id"]


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
        """
        Validates that the email is not already registered.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("EMAIL_ALREADY_REGISTERED")
        return value

    def save(self):
        """
        Validates matching passwords, creates the user and associated profile.
        """
        password = self.validated_data["password"]
        repeated_password = self.validated_data["repeated_password"]

        if password != repeated_password:
            raise serializers.ValidationError("PASSWORDS_DO_NOT_MATCH")

        user = User(
            email=self.validated_data["email"], username=self.validated_data["username"]
        )
        user.set_password(password)
        user.save()

        UserProfile.objects.create(user=user)

        Contact.objects.create(name=user.username, email=user.email, created_by=user)

        return user
