import uuid

from django.db import models

from core.exceptions import AppendOnlyViolation


class KarmaEventType(models.TextChoices):
    CONTRIBUTION_ACCEPTED = "contribution_accepted"
    CONTRIBUTION_REVERTED = "contribution_reverted"
    MILESTONE_BONUS = "milestone_bonus"
    VESTING = "vesting"
    MANUAL_ADJUSTMENT = "manual_adjustment"


class KarmaLedger(models.Model):
    """Append-only karma ledger. Updates and deletes are forbidden."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="karma_ledger_entries",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="karma_ledger_entries",
    )
    event_type = models.CharField(max_length=30, choices=KarmaEventType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=4)
    formula_inputs = models.JSONField(default=dict, blank=True)
    balance_after = models.DecimalField(max_digits=12, decimal_places=4)
    contribution = models.ForeignKey(
        "contributions.Contribution",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "karma_ledger"
        ordering = ["created_at"]

    def save(self, *args, **kwargs):
        if self.pk and KarmaLedger.objects.filter(pk=self.pk).exists():
            raise AppendOnlyViolation()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise AppendOnlyViolation()


class KarmaBalance(models.Model):
    """Denormalized karma balance per project per user. Rebuildable from ledger."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="karma_balances",
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="karma_balances",
    )
    total_karma = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    vested_karma = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    contribution_count = models.IntegerField(default=0)
    last_contribution_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "karma_balance"
        unique_together = [("project", "user")]
