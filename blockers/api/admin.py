from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id", "email",
        "full_name", "is_active",
        "is_superuser", "created_at",
        "updated_at"
    )
    

@admin.register(models.UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id", "user",
        "token", "expired_at",
        "created_at", "updated_at"
    )
    

@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name",
        "description",
        "image", "slug",
        "release_at", "created_by",
        "created_at", "updated_at"
    )
    

@admin.register(models.ProjectRelease)
class ProjectReleaseAdmin(admin.ModelAdmin):
    list_display = (
        "id", "project",
        "name", "release_at",
        "created_by", "created_at",
        "updated_at",
    )
    

@admin.register(models.ProjectSection)
class ProjectSectionAdmin(admin.ModelAdmin):
    list_display = (
        "id", "project", 
        "name", "created_by",
        "created_at",
        "updated_at"
    )
    
    
@admin.register(models.Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = (
        "id", "name", "color",
        "created_by", "created_at",
        "updated_at", "deleted_at"
    )
    
    
@admin.register(models.ProjectStatus)
class ProjectStatusAdmin(admin.ModelAdmin):
    list_display = (
        "id", "project",
        "status", "created_at",
        "updated_at"
    )
    

@admin.register(models.ProjectTask)
class ProjecTaskAdmin(admin.ModelAdmin):
    list_display = (
        "id", "section", "status",
        "name", "description",
        "start_at", "end_at",
        "created_by", "created_at",
        "updated_at"
    )
    

@admin.register(models.ProjectTaskEvent)
class ProjectTaskEventAdmin(admin.ModelAdmin):
    list_display = (
        "id", "task",
        "status", "created_by",
        "created_at", "updated_at"
    )