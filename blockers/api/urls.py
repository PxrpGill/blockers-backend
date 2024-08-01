from django.urls import path, include
from .views import ProjectViewSet, ProjectDetailViewSet, TaskViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = [
    path(
        "projects/<slug:slug>/",
        ProjectDetailViewSet.as_view({"get": "retrieve"}),
        name="project-detail",
    ),
    path(
        "projects/<slug:slug>/tasks/",
        TaskViewSet.as_view({"get": "list"}),
        name="project-tasks",
    ),
]

urlpatterns += router.urls
