from rest_framework import serializers
from .models import Project, ProjectTask, ProjectTaskEvent, ProjectRelease, Status


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ["id", "name", "color"]


class ProjectReleaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectRelease
        fields = ["id", "name", "release_at"]


class ProjectTaskEventSerializer(serializers.ModelSerializer):
    status = StatusSerializer()

    class Meta:
        model = ProjectTaskEvent
        fields = ["id", "status", "created_by", "created_at"]


class ProjectTaskSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    events = ProjectTaskEventSerializer(
        many=True, read_only=True, source="projecttaskevent_set"
    )

    class Meta:
        model = ProjectTask
        fields = ["id", "name", "description", "status", "events", "start_at", "end_at"]


class ProjectSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    releases = ProjectReleaseSerializer(
        many=True, read_only=True, source="projectrelease_set"
    )

    class Meta:
        model = Project
        fields = ["slug", "name", "status", "releases"]

    def get_status(self, obj):
        latest_status = obj.projectstatus_set.latest("created_at")
        return StatusSerializer(latest_status.status).data
