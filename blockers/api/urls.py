from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectDetailViewSet, TaskViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(
    r"projects/(?P<slug>[^/.]+)/detail", ProjectDetailViewSet, basename="project-detail"
)
router.register(
    r"projects/(?P<slug>[^/.]+)/tasks", TaskViewSet, basename="project-tasks"
)

urlpatterns = [
    path("", include(router.urls)),
]
