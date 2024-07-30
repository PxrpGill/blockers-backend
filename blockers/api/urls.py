from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ProjectTaskViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
    path(
        'projects/<slug:slug>/tasks/',
        ProjectTaskViewSet.as_view({'get': 'list'}),
        name='project-tasks',
    ),
]
