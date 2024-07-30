from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from .models import Project, ProjectTask, Status
from .serializers import ProjectSerializer, ProjectTaskSerializer
from rest_framework import status
from rest_framework.exceptions import NotFound


class ProjectPagination(PageNumberPagination):
    page_size_query_param = "perPage"


class ProjectTaskPagination(PageNumberPagination):
    page_size_query_param = "perPage"


class ProjectTaskViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    pagination_class = ProjectTaskPagination

    def list(self, request, *args, **kwargs):
        project_slug = kwargs.get("slug")
        try:
            project = Project.objects.get(slug=project_slug)
        except Project.DoesNotExist:
            raise NotFound("Project not found")

        self.queryset = self.queryset.filter(section__project=project)

        # Apply filters
        responsible = request.query_params.getlist("responsible[]")
        release = request.query_params.getlist("release[]")
        section = request.query_params.getlist("section[]")

        if responsible:
            self.queryset = self.queryset.filter(created_by__id__in=responsible)
        if release:
            self.queryset = self.queryset.filter(
                section__projectrelease__id__in=release
            )
        if section:
            self.queryset = self.queryset.filter(section__id__in=section)

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(self.queryset, many=True)
        return Response(serializer.data)

    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.page.number,
                "perPage": self.page.paginator.per_page,
                "count": self.page.paginator.count,
                "tasks": data,
            }
        )


class ProjectViewSet(viewsets.ViewSet):
    pagination_class = ProjectPagination
    lookup_field = 'slug'  # Указываем, что идентификатором является slug

    def list(self, request):
        status_name = request.query_params.get("status")
        queryset = Project.objects.all()

        if status_name:
            status = Status.objects.filter(name=status_name).first()
            if status:
                queryset = queryset.filter(projectstatus__status=status)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProjectSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, slug=None):
        try:
            project = Project.objects.get(slug=slug)
        except Project.DoesNotExist:
            raise NotFound("Project not found")
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=["get"], url_path="tasks")
    def tasks(self, request, slug=None):
        view = ProjectTaskViewSet.as_view({"get": "list"})
        return view(request, slug=slug)
