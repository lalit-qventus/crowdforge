import uuid

from django.conf import settings
from django.db import models


class VoteTargetType(models.TextChoices):
    PITCH = "pitch"
    CONTRIBUTION = "contribution"


class Vote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes"
    )
    target_type = models.CharField(max_length=20, choices=VoteTargetType.choices)
    target_id = models.UUIDField()
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "voting_vote"
        unique_together = [("voter", "target_type", "target_id")]
