from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django_filters import rest_framework as django_filters
from rest_framework import status
from .models import Project, ProjectTask, ProjectSection
from .serializers import ProjectsSerializer, ProjectDetailSerializer, TaskSerializer


class ProjectPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "perPage"
    max_page_size = 100


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectsSerializer
    pagination_class = ProjectPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ["status"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        response_data = {
            "page": int(request.query_params.get("page", 1)),
            "perPage": int(request.query_params.get("perPage", 10)),
            "count": self.get_queryset().count(),
            "projects": serializer.data,
        }
        return Response(response_data)


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        try:
            project = self.get_queryset().get(slug=slug)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(project)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        try:
            project = self.get_queryset().get(slug=slug)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(project, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        try:
            project = self.get_queryset().get(slug=slug)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        try:
            project = self.get_queryset().get(slug=slug)
        except Project.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(project)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({"items": data})


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = TaskPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.OrderingFilter)

    def get_queryset(self):
        project_slug = self.kwargs.get("slug")
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            return ProjectTask.objects.none()

        project_sections = ProjectSection.objects.filter(project=project)
        project_tasks = ProjectTask.objects.filter(section__in=project_sections)
        return project_tasks

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"items": serializer.data})
