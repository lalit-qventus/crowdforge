import uuid

from django.conf import settings
from django.db import models


class ContributionCategory(models.TextChoices):
    IDEATION = "ideation"
    CODE = "code"
    DESIGN = "design"
    TESTING = "testing"
    MARKETING = "marketing"
    SALES = "sales"
    GOVERNANCE = "governance"


class ContributionStatus(models.TextChoices):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    REVERTED = "reverted"


CONTRIBUTION_TRANSITIONS = {
    ContributionStatus.DRAFT: [ContributionStatus.SUBMITTED],
    ContributionStatus.SUBMITTED: [ContributionStatus.IN_REVIEW],
    ContributionStatus.IN_REVIEW: [
        ContributionStatus.ACCEPTED,
        ContributionStatus.REJECTED,
        ContributionStatus.CHANGES_REQUESTED,
    ],
    ContributionStatus.CHANGES_REQUESTED: [ContributionStatus.SUBMITTED],
    ContributionStatus.ACCEPTED: [ContributionStatus.REVERTED],
    ContributionStatus.REJECTED: [],
    ContributionStatus.REVERTED: [],
}


class Contribution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="contributions"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contributions"
    )
    task = models.ForeignKey(
        "tasks.Task",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="contributions",
    )
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, default="")
    category = models.CharField(max_length=20, choices=ContributionCategory.choices)
    external_pr_url = models.URLField(blank=True, default="")
    diff_summary = models.TextField(blank=True, default="")
    status = models.CharField(
        max_length=20, choices=ContributionStatus.choices, default=ContributionStatus.DRAFT
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reviewed_contributions",
    )
    review_note = models.TextField(blank=True, default="")

    # Karma fields -- frozen at computation time
    base_karma = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    pioneer_multiplier = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    upvote_score = models.DecimalField(max_digits=10, decimal_places=4, default=0)
    ai_multiplier = models.DecimalField(max_digits=10, decimal_places=4, default=1)
    karma_awarded = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    karma_vested = models.DecimalField(max_digits=12, decimal_places=4, default=0)

    submitted_at = models.DateTimeField(null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    reverted_at = models.DateTimeField(null=True, blank=True)
    reverted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reverted_contributions",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "contributions_contribution"

    def __str__(self):
        return self.title
