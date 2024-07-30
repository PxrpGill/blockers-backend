from django.db import models
import uuid


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=320, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=255)
    team = models.CharField(max_length=32, help_text="Команда пользователя")
    role = models.CharField(max_length=32, default="role_user")
    password = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="user_created_by",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="user_updated_by",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class Project(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("develop", "Develop"),
        ("released", "Released"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    name = models.CharField(max_length=255)
    jira_id = models.CharField(max_length=32, null=True, blank=True)
    slug = models.SlugField(max_length=32, unique=True)
    release = models.ForeignKey(
        "ProjectRelease", null=True, blank=True, on_delete=models.SET_NULL
    )
    released_at = models.DateTimeField()
    created_by = models.ForeignKey(
        User, related_name="project_created_by", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name="project_updated_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        User, related_name="project_section_created_by", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name="project_section_updated_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectRelease(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    comment = models.CharField(max_length=512, null=True, blank=True)
    released_at = models.DateTimeField()
    created_by = models.ForeignKey(
        User, related_name="project_release_created_by", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name="project_release_updated_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=12)
    created_by = models.ForeignKey(
        User, related_name="status_created_by", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name="status_updated_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProjectTask(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    section = models.ForeignKey(ProjectSection, on_delete=models.CASCADE)
    release = models.ForeignKey(
        ProjectRelease, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=255)
    comment = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="project_task_created_by", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name="project_task_updated_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProjectTaskEvent(models.Model):
    RISK_CHOICES = [
        ("done", "Готово"),
        ("have_blocker", "Есть блокеры"),
        ("no_risk", "Нет рисков"),
    ]

    TYPE_CHOICES = [
        ("done", "Выполнено"),
        ("transfer", "Перенос"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(ProjectTask, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    responsible = models.ForeignKey(
        User, related_name="project_task_event_responsible", on_delete=models.CASCADE
    )
    risk = models.CharField(max_length=32, choices=RISK_CHOICES)
    type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    comment = models.TextField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, related_name="project_task_event_created_by", on_delete=models.CASCADE
    )
    updated_by = models.ForeignKey(
        User, related_name="project_task_event_updated_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Event for Task {self.task.name}"


class UserProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "project")


class UserToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
    expired_at = models.DateTimeField()
    created_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="user_token_created_by",
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        related_name="user_token_updated_by",
        on_delete=models.SET_NULL,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Token for User {self.user.email}"


class ProjectStatus(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("project", "status")
