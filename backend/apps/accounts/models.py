import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class User(AbstractUser):
    class TrustLevel(models.IntegerChoices):
        OBSERVER = 0, "Observer"
        PARTICIPANT = 1, "Participant"
        CONTRIBUTOR = 2, "Contributor"
        TRUSTED = 3, "Trusted"
        STEWARD = 4, "Steward"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    identity_score = models.IntegerField(default=0)
    trust_level = models.IntegerField(
        choices=TrustLevel.choices, default=TrustLevel.OBSERVER
    )
    is_ai_agent = models.BooleanField(default=False)
    parent_user = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="ai_agents",
    )
    fraud_risk_tier = models.CharField(max_length=20, default="low")
    fraud_score = models.IntegerField(default=0)
    is_shadow_restricted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = "accounts_user"


class VerificationMethod(models.TextChoices):
    EMAIL = "email"
    PHONE_SMS = "phone_sms"
    SOCIAL_OAUTH = "social_oauth"
    GITHUB_HISTORY = "github_history"
    WORLD_ID = "world_id"
    VOUCHING = "vouching"


class UserVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="verifications"
    )
    method = models.CharField(max_length=30, choices=VerificationMethod.choices)
    provider_user_id = models.CharField(max_length=255, blank=True, default="")
    score_awarded = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "accounts_user_verification"
        unique_together = [("user", "method")]


class Vouch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    voucher = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vouches_given"
    )
    vouchee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="vouches_received"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "accounts_vouch"
        unique_together = [("voucher", "vouchee")]
