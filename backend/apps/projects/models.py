import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class LifecycleStage(models.TextChoices):
    PROPOSAL = "proposal"
    INCUBATION = "incubation"
    ACTIVE_BUILD = "active_build"
    SHIPPED = "shipped"
    EARNING = "earning"
    SUNSET = "sunset"


# Valid lifecycle transitions
LIFECYCLE_TRANSITIONS = {
    LifecycleStage.PROPOSAL: [LifecycleStage.INCUBATION],
    LifecycleStage.INCUBATION: [LifecycleStage.ACTIVE_BUILD],
    LifecycleStage.ACTIVE_BUILD: [LifecycleStage.SHIPPED],
    LifecycleStage.SHIPPED: [LifecycleStage.EARNING, LifecycleStage.SUNSET],
    LifecycleStage.EARNING: [LifecycleStage.SUNSET],
    LifecycleStage.SUNSET: [],
}


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    one_liner = models.CharField(max_length=300, blank=True, default="")
    problem = models.TextField(blank=True, default="")
    solution = models.TextField(blank=True, default="")
    target_user = models.TextField(blank=True, default="")
    revenue_model = models.TextField(blank=True, default="")
    tech_stack_tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)
    lifecycle_stage = models.CharField(max_length=20, choices=LifecycleStage.choices, default=LifecycleStage.PROPOSAL)

    # Lifecycle timestamps
    proposal_ends_at = models.DateTimeField(null=True, blank=True)
    incubation_started_at = models.DateTimeField(null=True, blank=True)
    active_build_started_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    sunset_at = models.DateTimeField(null=True, blank=True)

    founder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="founded_projects")
    production_url = models.URLField(blank=True, default="")
    staging_url = models.URLField(blank=True, default="")
    repo_url = models.URLField(blank=True, default="")

    # Per-project tunable parameters
    settings = models.JSONField(default=dict, blank=True)

    # Milestone counters
    accepted_contributions = models.IntegerField(default=0)
    unique_contributors = models.IntegerField(default=0)
    first_revenue = models.BooleanField(default=False)
    milestone_1_reached = models.BooleanField(default=False)
    milestone_2_reached = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = "projects_project"

    def __str__(self):
        return self.title


class ProjectMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    is_seed_team = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    removed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "projects_project_member"
        unique_together = [("project", "user")]
