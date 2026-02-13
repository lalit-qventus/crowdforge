import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class TaskStatus(models.TextChoices):
    OPEN = "open"
    CLAIMED = "claimed"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskEffort(models.TextChoices):
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"


class ContributionCategory(models.TextChoices):
    IDEATION = "ideation"
    CODE = "code"
    DESIGN = "design"
    TESTING = "testing"
    MARKETING = "marketing"
    SALES = "sales"
    GOVERNANCE = "governance"


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="tasks")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_tasks")
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")
    acceptance_criteria = models.TextField(blank=True, default="")
    category = models.CharField(max_length=20, choices=ContributionCategory.choices)
    estimated_effort = models.CharField(max_length=2, choices=TaskEffort.choices, default=TaskEffort.MEDIUM)
    required_skills = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    karma_bounty = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    is_critical = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.OPEN)
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="assigned_tasks")
    claimed_at = models.DateTimeField(null=True, blank=True)
    claim_expires_at = models.DateTimeField(null=True, blank=True)
    extended_once = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = "tasks_task"

    def __str__(self):
        return self.title
