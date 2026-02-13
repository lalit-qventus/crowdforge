import uuid

from django.conf import settings
from django.db import models


class EventType(models.TextChoices):
    PROJECT_CREATED = "project_created"
    PROJECT_TRANSITIONED = "project_transitioned"
    MEMBER_JOINED = "member_joined"
    CONTRIBUTION_SUBMITTED = "contribution_submitted"
    CONTRIBUTION_ACCEPTED = "contribution_accepted"
    CONTRIBUTION_REJECTED = "contribution_rejected"
    CONTRIBUTION_REVERTED = "contribution_reverted"
    TASK_CREATED = "task_created"
    TASK_CLAIMED = "task_claimed"
    TASK_COMPLETED = "task_completed"
    KARMA_AWARDED = "karma_awarded"
    VOTE_CAST = "vote_cast"
    USER_REGISTERED = "user_registered"
    VERIFICATION_ADDED = "verification_added"


class ActivityEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_type = models.CharField(max_length=40, choices=EventType.choices)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activity_events"
    )
    project = models.ForeignKey(
        "projects.Project",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="activity_events",
    )
    target_type = models.CharField(max_length=50, blank=True, default="")
    target_id = models.UUIDField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)

    # Denormalized for fast reads
    actor_username = models.CharField(max_length=150, blank=True, default="")
    actor_avatar_url = models.URLField(blank=True, default="")
    project_slug = models.CharField(max_length=100, blank=True, default="")
    project_title = models.CharField(max_length=200, blank=True, default="")
    summary = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "activity_event"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["project", "-created_at"]),
            models.Index(fields=["actor", "-created_at"]),
        ]
