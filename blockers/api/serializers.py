from rest_framework import serializers
from . import models


class ResponsibleSerializer(serializers.ModelSerializer):
    fullName = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = ("id", "fullName", "team")

    def get_fullName(self, obj):
        return obj.full_name


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = ("id", "name", "color")


class ProjectReleaseSerializer(serializers.ModelSerializer):
    released = serializers.SerializerMethodField()

    class Meta:
        model = models.ProjectRelease
        fields = ("id", "name", "comment", "released")

    def get_released(self, obj):
        if obj.released_at:
            return obj.released_at.strftime("%Y-%m-%d")
        return None


class ProjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectSection
        fields = ("id", "name")


class ProjectDetailSerializer(serializers.ModelSerializer):
    statuses = serializers.SerializerMethodField()
    releases = serializers.SerializerMethodField()
    responsibles = serializers.SerializerMethodField()
    sections = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = (
            "slug",
            "name",
            "status",
            "statuses",
            "releases",
            "responsibles",
            "sections",
        )

    def get_sections(self, obj):
        sections = models.ProjectSection.objects.filter(project=obj)
        return ProjectSectionSerializer(sections, many=True).data

    def get_responsibles(self, obj):
        responsibles = models.User.objects.all()
        return ResponsibleSerializer(responsibles, many=True).data

    def get_releases(self, obj):
        releases = models.ProjectRelease.objects.all()
        return ProjectReleaseSerializer(releases, many=True).data

    def get_statuses(self, obj):
        statuses = models.Status.objects.all()
        return StatusSerializer(statuses, many=True).data

    def get_status(self, obj):
        status = obj.status
        color = ""

        if status == "New":
            color = "#f7f7f7"

        elif status == "Develop":
            color = "#65E6AC"

        else:
            color = "#79E665"

        return {"name": status, "color": color}


class ProjectsSerializer(serializers.ModelSerializer):
    release = ProjectReleaseSerializer()
    status = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = ("slug", "name", "status", "release")

    def get_status(self, obj):
        status = obj.status
        color = ""

        if status == "new":
            color = "#f7f7f7"

        elif status == "develop":
            color = "#65E6AC"

        else:
            color = "#79E665"

        return {"name": status, "color": color}


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectSection
        fields = ("id", "name")


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectRelease
        fields = ("id", "name", "released_at")


class EventResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id", "full_name")


class EventSerializer(serializers.ModelSerializer):
    responsible = serializers.UUIDField(source="responsible.id")
    startedAt = serializers.SerializerMethodField()
    endedAt = serializers.SerializerMethodField()

    class Meta:
        model = models.ProjectTaskEvent
        fields = (
            "id",
            "responsible",
            "comment",
            "risk",
            "type",
            "startedAt",
            "endedAt",
        )

    def get_startedAt(self, obj):
        if obj.started_at:
            return obj.started_at.strftime("%Y-%m-%d")
        return None

    def get_endedAt(self, obj):
        if obj.ended_at:
            return obj.ended_at.strftime("%Y-%m-%d")
        return None


class TaskSerializer(serializers.ModelSerializer):
    section = serializers.UUIDField(source="section.id")
    release = serializers.UUIDField(source="release.id")
    status = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()

    class Meta:
        model = models.ProjectTask
        fields = (
            "id",
            "name",
            "comment",
            "section",
            "release",
            "status",
            "events",
        )

    def get_status(self, obj):
        latest_event = obj.projecttaskevent_set.order_by("-created_at").first()
        if latest_event:
            return latest_event.status.id
        return None

    def get_events(self, obj):
        events = models.ProjectTaskEvent.objects.filter(task=obj)
        return EventSerializer(events, many=True).data
