from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "full_name",
        "team",
        "role",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "name",
        "jira_id",
        "release",
        "released_at",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


@admin.register(models.ProjectSection)
class ProjectSectionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "project",
        "name",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


@admin.register(models.ProjectRelease)
class ProjectReleaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "released_at",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


@admin.register(models.ProjectTask)
class ProjectTask(admin.ModelAdmin):
    list_display = (
        "id",
        "is_active",
        "section",
        "release",
        "name",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(models.ProjectTaskEvent)
class ProjectTaskEventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "task",
        "status",
        "responsible",
        "risk",
        "type",
        "started_at",
        "ended_at",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
        "deleted_at",
    )


@admin.register(models.UserProject)
class UserProjectAdmin(admin.ModelAdmin):
    list_display = ("user", "project")


@admin.register(models.UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "token",
        "expired_at",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )


@admin.register(models.ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "status",
    )
