from decimal import Decimal

from django.db.models import F
from django.utils import timezone

from core.constants import (
    AI_MAX_CONTRIBUTIONS_PER_PROJECT_DAY_ACTIVE,
    AI_MAX_SIMULTANEOUS_ACTIVE_BUILD_PROJECTS,
    BASE_KARMA,
    CONTRIBUTION_RATE_LIMITS,
    REVIEWER_MIN_PROJECT_KARMA,
    TrustLevel,
)
from core.events import publish_project_event
from core.exceptions import BadRequest, InsufficientKarma, InvalidStateTransition, PermissionDenied, RateLimited

from apps.karma.models import KarmaBalance
from apps.karma import services as karma_services
from apps.karma.formulas import pioneer_multiplier as compute_pioneer_multiplier
from apps.projects.models import Project, ProjectMember

from .models import Contribution, ContributionStatus, CONTRIBUTION_TRANSITIONS


def create_contribution(author, data) -> Contribution:
    project = Project.objects.get(id=data.project_id)

    if not ProjectMember.objects.filter(project=project, user=author, removed_at__isnull=True).exists():
        raise PermissionDenied("Must be a project member to contribute")

    trust_level = TrustLevel(author.trust_level)
    daily_limit = CONTRIBUTION_RATE_LIMITS.get(trust_level, 0)
    if get_user_daily_submission_count(author, project) >= daily_limit:
        raise RateLimited(f"Daily submission limit ({daily_limit}) reached for trust level {trust_level.name}")

    if author.is_ai_agent:
        check_ai_constraints(author, project)

    base = BASE_KARMA.get(data.category, Decimal("5"))

    contribution = Contribution.objects.create(
        project=project,
        author=author,
        task_id=data.task_id,
        title=data.title,
        description=data.description,
        category=data.category,
        external_pr_url=data.external_pr_url,
        diff_summary=data.diff_summary,
        base_karma=base,
    )

    publish_project_event(
        project.id,
        "contribution.created",
        {"contribution_id": str(contribution.id), "author_id": str(author.id)},
    )

    return contribution


def update_contribution(contribution, user, data) -> Contribution:
    if contribution.author_id != user.id:
        raise PermissionDenied("Only the author can update a contribution")
    if contribution.status != ContributionStatus.DRAFT:
        raise BadRequest("Can only update contributions in draft status")

    if data.title is not None:
        contribution.title = data.title
    if data.description is not None:
        contribution.description = data.description
    if data.external_pr_url is not None:
        contribution.external_pr_url = data.external_pr_url
    if data.diff_summary is not None:
        contribution.diff_summary = data.diff_summary

    contribution.save()
    return contribution


def submit_contribution(contribution, user) -> Contribution:
    if contribution.author_id != user.id:
        raise PermissionDenied("Only the author can submit a contribution")

    _validate_transition(contribution.status, ContributionStatus.SUBMITTED)

    now = timezone.now()
    contribution.status = ContributionStatus.SUBMITTED
    contribution.submitted_at = now

    # Freeze pioneer multiplier at submission time
    days = 0
    if contribution.project.incubation_started_at:
        days = (now - contribution.project.incubation_started_at).days
    contribution.pioneer_multiplier = compute_pioneer_multiplier(days)

    contribution.save(update_fields=["status", "submitted_at", "pioneer_multiplier", "updated_at"])

    publish_project_event(
        contribution.project_id,
        "contribution.submitted",
        {"contribution_id": str(contribution.id), "author_id": str(user.id)},
    )

    return contribution


def start_review(contribution, reviewer) -> Contribution:
    if reviewer.id == contribution.author_id:
        raise PermissionDenied("Self-review is not allowed")

    _validate_transition(contribution.status, ContributionStatus.IN_REVIEW)

    balance = KarmaBalance.objects.filter(
        project=contribution.project, user=reviewer
    ).first()
    reviewer_karma = balance.total_karma if balance else Decimal("0")
    if reviewer_karma < REVIEWER_MIN_PROJECT_KARMA:
        raise InsufficientKarma(REVIEWER_MIN_PROJECT_KARMA)

    contribution.reviewer = reviewer
    contribution.status = ContributionStatus.IN_REVIEW
    contribution.save(update_fields=["reviewer", "status", "updated_at"])

    return contribution


def review_contribution(contribution, reviewer, action, review_note="") -> Contribution:
    if contribution.reviewer_id != reviewer.id:
        raise PermissionDenied("Only the assigned reviewer can decide")

    if action == "accept":
        _validate_transition(contribution.status, ContributionStatus.ACCEPTED)
        contribution.status = ContributionStatus.ACCEPTED
        contribution.accepted_at = timezone.now()
        contribution.review_note = review_note
        contribution.save(update_fields=["status", "accepted_at", "review_note", "updated_at"])

        karma_services.award_contribution_karma(contribution)

        # Update project milestone counters
        project = contribution.project
        project.accepted_contributions = F("accepted_contributions") + 1
        project.save(update_fields=["accepted_contributions"])
        project.refresh_from_db(fields=["accepted_contributions"])

        # Update unique contributors count
        unique_count = (
            Contribution.objects.filter(project=project, status=ContributionStatus.ACCEPTED)
            .values("author")
            .distinct()
            .count()
        )
        project.unique_contributors = unique_count
        project.save(update_fields=["unique_contributors"])

        publish_project_event(
            project.id,
            "contribution.accepted",
            {
                "contribution_id": str(contribution.id),
                "reviewer_id": str(reviewer.id),
                "karma_awarded": str(contribution.karma_awarded),
            },
        )

    elif action == "reject":
        _validate_transition(contribution.status, ContributionStatus.REJECTED)
        contribution.status = ContributionStatus.REJECTED
        contribution.rejected_at = timezone.now()
        contribution.review_note = review_note
        contribution.save(update_fields=["status", "rejected_at", "review_note", "updated_at"])

        publish_project_event(
            contribution.project_id,
            "contribution.rejected",
            {"contribution_id": str(contribution.id), "reviewer_id": str(reviewer.id)},
        )

    elif action == "request_changes":
        _validate_transition(contribution.status, ContributionStatus.CHANGES_REQUESTED)
        contribution.status = ContributionStatus.CHANGES_REQUESTED
        contribution.review_note = review_note
        contribution.save(update_fields=["status", "review_note", "updated_at"])

        publish_project_event(
            contribution.project_id,
            "contribution.changes_requested",
            {"contribution_id": str(contribution.id), "reviewer_id": str(reviewer.id)},
        )

    else:
        raise BadRequest(f"Invalid review action: {action}")

    return contribution


def revert_contribution(contribution, reverter, reason) -> Contribution:
    _validate_transition(contribution.status, ContributionStatus.REVERTED)

    karma_services.penalize_revert(contribution)

    contribution.status = ContributionStatus.REVERTED
    contribution.reverted_at = timezone.now()
    contribution.reverted_by = reverter
    contribution.review_note = reason
    contribution.save(
        update_fields=["status", "reverted_at", "reverted_by", "review_note", "updated_at"]
    )

    publish_project_event(
        contribution.project_id,
        "contribution.reverted",
        {
            "contribution_id": str(contribution.id),
            "reverter_id": str(reverter.id),
            "reason": reason,
        },
    )

    return contribution


def get_user_daily_submission_count(user, project) -> int:
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    return Contribution.objects.filter(
        author=user,
        project=project,
        submitted_at__gte=today_start,
    ).exclude(
        status=ContributionStatus.DRAFT,
    ).count()


def check_ai_constraints(user, project):
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)

    if project.lifecycle_stage == "active_build":
        daily_count = Contribution.objects.filter(
            author=user,
            project=project,
            created_at__gte=today_start,
        ).count()
        if daily_count >= AI_MAX_CONTRIBUTIONS_PER_PROJECT_DAY_ACTIVE:
            raise RateLimited(
                f"AI agents limited to {AI_MAX_CONTRIBUTIONS_PER_PROJECT_DAY_ACTIVE} "
                f"contributions per project per day during active build"
            )

    active_build_project_count = (
        Contribution.objects.filter(
            author=user,
            project__lifecycle_stage="active_build",
            created_at__gte=today_start,
        )
        .values("project")
        .distinct()
        .count()
    )
    # Count the current project if it's active_build and not yet counted
    if project.lifecycle_stage == "active_build":
        existing = Contribution.objects.filter(
            author=user, project=project, created_at__gte=today_start
        ).exists()
        if not existing:
            active_build_project_count += 1

    if active_build_project_count > AI_MAX_SIMULTANEOUS_ACTIVE_BUILD_PROJECTS:
        raise RateLimited(
            f"AI agents limited to {AI_MAX_SIMULTANEOUS_ACTIVE_BUILD_PROJECTS} "
            f"simultaneous active build projects"
        )


def _validate_transition(current_status, target_status):
    allowed = CONTRIBUTION_TRANSITIONS.get(current_status, [])
    if target_status not in allowed:
        raise InvalidStateTransition(current_status, target_status)
