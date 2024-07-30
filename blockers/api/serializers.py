from rest_framework import serializers

from . import models


class ResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id", "full_name", "team")


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = ("id", "name", "color")


class ProjectReleaseSerializer(serializers.ModelSerializer):
    released = serializers.SerializerMethodField()

    class Meta:
        model = models.ProjectRelease
        fields = ("id", "name", "comment", "released")

    def get_release_date(self, obj):
        if obj.released_at:
            return obj.released_at.strftime("%Y-%m-%d")
        return None


class ProjectSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectSection
        fields = ("id", "name")


class ProjectDetailSerializer(serializers.ModelSerializer):
    statuses = StatusSerializer(many=True)
    releases = ProjectReleaseSerializer(many=True)
    responsibles = ResponsibleSerializer(many=True)
    sections = ProjectSectionSerializer(many=True)
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

        if status == "New":
            color = "#f7f7f7"

        elif status == "Develop":
            color = "#65E6AC"

        else:
            color = "#79E665"

        return {"name": status, "color": color}


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectSection
        fields = ("id",)


class ReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectRelease
        fields = ("id",)


class EventResponsibleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id",)


class EventSerializer(serializers.ModelSerializer):
    responsible = EventResponsibleSerializer()
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

    def get_started_at_date(self, obj):
        if obj.started_at:
            return obj.started_at.strftime("%Y-%m-%d")
        return None

    def get_ended_at_date(self, obj):
        if obj.ended_at:
            return obj.ended_at.strftime("%Y-%m-%d")
        return None


class TaskSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    release = ReleaseSerializer()
    status = StatusSerializer()

    class Meta:
        model = models.ProjectTask
        fields = ("id", "name", "comment", "section", "release", "status")
