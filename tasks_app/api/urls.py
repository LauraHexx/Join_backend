from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet, SubtaskViewSet, SummaryViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"subtasks", SubtaskViewSet, basename="subtask")
router.register(r"summary", SummaryViewSet, basename="summary")


urlpatterns = [
    path("", include(router.urls)),
]
