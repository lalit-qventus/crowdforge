from decimal import Decimal

from django.db import IntegrityError
from django.utils import timezone

from core.constants import (
    FOUNDER_SELF_VOTE_WEIGHT,
    IDEA_RING_QUORUM,
    IDEA_RING_THRESHOLD,
    SELF_VOTE_WEIGHT,
)
from core.events import publish_project_event
from core.exceptions import BadRequest, Conflict, PermissionDenied

from apps.projects.models import Project, LifecycleStage

from .models import Vote, VoteTargetType


def cast_vote(voter, target_type, target_id) -> Vote:
    if voter.is_ai_agent:
        raise PermissionDenied("AI agents cannot vote")

    if target_type == VoteTargetType.PITCH:
        project = Project.objects.get(id=target_id)

        if project.proposal_ends_at and timezone.now() > project.proposal_ends_at:
            raise BadRequest("Voting window has closed")

        weight = Decimal("1.0")
        if voter.id == project.founder_id:
            weight = FOUNDER_SELF_VOTE_WEIGHT

    elif target_type == VoteTargetType.CONTRIBUTION:
        from apps.contributions.models import Contribution
        contribution = Contribution.objects.get(id=target_id)

        weight = Decimal("1.0")
        if voter.id == contribution.author_id:
            weight = SELF_VOTE_WEIGHT

    else:
        raise BadRequest(f"Invalid target type: {target_type}")

    try:
        vote = Vote.objects.create(
            voter=voter,
            target_type=target_type,
            target_id=target_id,
            weight=weight,
        )
    except IntegrityError:
        raise Conflict("You have already voted on this item")

    if target_type == VoteTargetType.PITCH:
        check_idea_ring_threshold(project)
        channel_id = target_id
    else:
        channel_id = contribution.project_id

    publish_project_event(
        channel_id,
        "vote.cast",
        {
            "voter_id": str(voter.id),
            "target_type": target_type,
            "target_id": str(target_id),
        },
    )

    return vote


def check_idea_ring_threshold(project) -> bool:
    votes = Vote.objects.filter(
        target_type=VoteTargetType.PITCH, target_id=project.id
    )
    vote_count = votes.count()

    if vote_count < IDEA_RING_QUORUM:
        return False

    total_weight = sum(v.weight for v in votes)
    max_possible = Decimal(str(vote_count))
    weighted_ratio = total_weight / max_possible if max_possible > 0 else Decimal("0")

    if weighted_ratio >= IDEA_RING_THRESHOLD:
        if project.lifecycle_stage == LifecycleStage.PROPOSAL:
            project.lifecycle_stage = LifecycleStage.INCUBATION
            project.incubation_started_at = timezone.now()
            project.save(update_fields=["lifecycle_stage", "incubation_started_at", "updated_at"])

            publish_project_event(
                project.id,
                "project.transitioned",
                {"from": "proposal", "to": "incubation", "trigger": "idea_ring"},
            )
            return True

    return False


def get_idea_ring_status(project) -> dict:
    votes = Vote.objects.filter(
        target_type=VoteTargetType.PITCH, target_id=project.id
    )
    vote_count = votes.count()
    total_weight = sum(v.weight for v in votes)
    max_possible = Decimal(str(vote_count))
    weighted_ratio = total_weight / max_possible if max_possible > 0 else Decimal("0")

    return {
        "project_id": project.id,
        "total_votes": vote_count,
        "weighted_score": total_weight,
        "quorum_met": vote_count >= IDEA_RING_QUORUM,
        "threshold_met": weighted_ratio >= IDEA_RING_THRESHOLD,
        "vote_count": vote_count,
    }


def get_contribution_upvote_count(contribution_id) -> int:
    return Vote.objects.filter(
        target_type=VoteTargetType.CONTRIBUTION, target_id=contribution_id
    ).count()
