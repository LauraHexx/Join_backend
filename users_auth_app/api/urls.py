from django.urls import path
from .views import (
    UserProfileList,
    UserProfileDetail,
    LoginView,
    RegistrationView,
    GuestLoginView,
    LogoutView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", UserProfileList.as_view(), name="userprofile-list"),
    path("users/<int:pk>/", UserProfileDetail.as_view(), name="userprofile-detail"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    path("guest-login/", GuestLoginView.as_view(), name="guest-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
