from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import generics

from django.contrib.auth.models import User
from .serializers import UserProfileSerializer, RegistrationSerializer
from dummy_data_app.api.utils import create_dummy_data
from .utils import generate_random_password, get_next_guest_credentials


class UserProfileList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()

    def get_serializer_class(self):
        """
        Returns the appropriate serializer based on the request method.
        """
        if self.request.method == "POST":
            return RegistrationSerializer
        return UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles user registration using the RegistrationSerializer.
        """
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            data = self.create_response_data(saved_account)
            create_dummy_data(saved_account)
        else:
            data = serializer.errors
        return Response(data)

    def create_response_data(self, saved_account):
        """
        Creates response data including authentication token.
        """
        token, created = Token.objects.get_or_create(user=saved_account)
        return {
            "token": token.key,
            "username": saved_account.username,
            "email": saved_account.email,
            "id": saved_account.id,
        }


class GuestLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        guest_password = generate_random_password()
        username, email = get_next_guest_credentials()

        guest_data = {
            "username": username,
            "email": email,
            "password": guest_password,
            "repeated_password": guest_password,
        }

        serializer = RegistrationSerializer(data=guest_data)

        if serializer.is_valid():
            saved_account = serializer.save()
            data = self.create_response_data(saved_account)
            create_dummy_data(saved_account)
        else:
            data = serializer.errors

        return Response(data)

    def create_response_data(self, saved_account):
        token, created = Token.objects.get_or_create(user=saved_account)
        return {
            "token": token.key,
            "username": saved_account.username,
            "email": saved_account.email,
            "id": saved_account.id,
        }


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Authenticates the user and returns an authentication token.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            data = self.create_response_data(user)
        else:
            data = serializer.errors

        return Response(data)

    def create_response_data(self, user):
        """
        Creates the response data including the token and basic user info.
        """
        token, created = Token.objects.get_or_create(user=user)
        return {
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "id": user.id,
        }


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Logs out the user by deleting the auth token.
        """
        try:
            request.user.auth_token.delete()
            return Response({"message": "Successfully logged out."}, status=200)
        except (AttributeError, Token.DoesNotExist):
            return Response({"error": "No active session found."}, status=400)
