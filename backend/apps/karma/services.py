from decimal import Decimal

from django.db import models
from django.db.models import F, Sum
from django.utils import timezone

from core.constants import (
    AI_KARMA_MULTIPLIER_ACTIVE_BUILD,
    AI_KARMA_MULTIPLIER_DEFAULT,
    BASE_KARMA,
    REVERT_PENALTY_MULTIPLIER,
)
from core.events import publish_project_event

from .formulas import contribution_karma, pioneer_multiplier, upvote_score
from .models import KarmaBalance, KarmaEventType, KarmaLedger


def award_contribution_karma(contribution):
    project = contribution.project
    user = contribution.author

    base = BASE_KARMA.get(contribution.category, Decimal("5"))

    days = 0
    if project.incubation_started_at and contribution.submitted_at:
        days = (contribution.submitted_at - project.incubation_started_at).days

    pioneer = pioneer_multiplier(days)

    from apps.voting.services import get_contribution_upvote_count
    vote_count = get_contribution_upvote_count(contribution.id)
    upvote = upvote_score(vote_count)

    ai_mult = AI_KARMA_MULTIPLIER_DEFAULT
    if user.is_ai_agent and getattr(project, "lifecycle_stage", "") == "active_build":
        ai_mult = AI_KARMA_MULTIPLIER_ACTIVE_BUILD

    karma = contribution_karma(base, pioneer, upvote, ai_mult)

    balance, _ = KarmaBalance.objects.get_or_create(
        project=project, user=user, defaults={"total_karma": Decimal("0")}
    )
    new_total = balance.total_karma + karma

    entry = KarmaLedger.objects.create(
        project=project,
        user=user,
        event_type=KarmaEventType.CONTRIBUTION_ACCEPTED,
        amount=karma,
        balance_after=new_total,
        contribution=contribution,
        formula_inputs={
            "base": str(base),
            "pioneer_days": days,
            "pioneer_multiplier": str(pioneer),
            "upvote_count": vote_count,
            "upvote_score": str(upvote),
            "ai_multiplier": str(ai_mult),
        },
        description=f"Karma for contribution {contribution.id}",
    )

    balance.total_karma = new_total
    balance.contribution_count = F("contribution_count") + 1
    balance.last_contribution_at = timezone.now()
    balance.save(update_fields=["total_karma", "contribution_count", "last_contribution_at"])

    contribution.karma_awarded = karma
    contribution.save(update_fields=["karma_awarded"])

    publish_project_event(
        project.id,
        "karma.awarded",
        {
            "user_id": str(user.id),
            "contribution_id": str(contribution.id),
            "amount": str(karma),
        },
    )

    return entry


def penalize_revert(contribution):
    project = contribution.project
    user = contribution.author
    original_karma = contribution.karma_awarded or Decimal("0")
    penalty = original_karma * REVERT_PENALTY_MULTIPLIER

    balance = KarmaBalance.objects.get(project=project, user=user)
    new_total = balance.total_karma - penalty

    entry = KarmaLedger.objects.create(
        project=project,
        user=user,
        event_type=KarmaEventType.CONTRIBUTION_REVERTED,
        amount=-penalty,
        balance_after=new_total,
        contribution=contribution,
        description=f"Revert penalty for contribution {contribution.id}",
    )

    balance.total_karma = new_total
    balance.save(update_fields=["total_karma"])

    publish_project_event(
        project.id,
        "karma.reverted",
        {
            "user_id": str(user.id),
            "contribution_id": str(contribution.id),
            "penalty": str(penalty),
        },
    )

    return entry


def recalculate_project(project):
    """Replay all ledger entries and verify/fix KarmaBalance rows."""
    balances: dict[str, Decimal] = {}

    entries = KarmaLedger.objects.filter(project=project).order_by("created_at")
    for entry in entries:
        key = str(entry.user_id)
        balances[key] = balances.get(key, Decimal("0")) + entry.amount

    for user_id_str, expected_total in balances.items():
        KarmaBalance.objects.update_or_create(
            project=project,
            user_id=user_id_str,
            defaults={"total_karma": expected_total},
        )


def get_balance(project, user) -> KarmaBalance:
    balance, _ = KarmaBalance.objects.get_or_create(
        project=project, user=user, defaults={"total_karma": Decimal("0")}
    )
    return balance


def get_project_leaderboard(project):
    return KarmaBalance.objects.filter(project=project).order_by("-total_karma")
