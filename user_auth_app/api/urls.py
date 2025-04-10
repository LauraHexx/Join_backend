from django.urls import path
from .views import UserProfileList, UserProfileDetail, LoginView, RegistrationView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("profiles/", UserProfileList.as_view(), name="userprofile-list"),
    path("profiles/<int:pk>/", UserProfileDetail.as_view(), name="userprofile-detail"),
    path("registration/", RegistrationView.as_view(), name="registration"),
    path("login/", LoginView.as_view(), name="login"),
    # path("login/", obtain_auth_token, name="login"),
]
