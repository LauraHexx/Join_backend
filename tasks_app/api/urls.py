from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, SubtaskViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"subtasks", SubtaskViewSet, basename="subtask")


urlpatterns = [
    path("", include(router.urls)),
]
