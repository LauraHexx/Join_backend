from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import ContactViewSet, CategoryViewSet


router = routers.SimpleRouter()

router.register(r"contacts", ContactViewSet)
router.register(r"categorys", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
