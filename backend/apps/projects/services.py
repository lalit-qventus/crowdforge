from datetime import timedelta
from uuid import UUID

from django.db.models import QuerySet
from django.utils import timezone

from core.constants import (
    PIONEER_BONUS_MAX,
    PIONEER_BONUS_MIN,
    PIONEER_DECAY_MAX,
    PIONEER_DECAY_MIN,
    PROPOSAL_BUFFER_HOURS,
    TrustLevel,
)
from core.events import publish_project_event
from core.exceptions import (
    BadRequest,
    Conflict,
    InvalidStateTransition,
    NotFound,
    PermissionDenied,
)

from .models import (
    LIFECYCLE_TRANSITIONS,
    LifecycleStage,
    Project,
    ProjectMember,
)


def validate_project_settings(settings_dict: dict) -> dict:
    """Validate per-project tunable parameters."""
    from decimal import Decimal

    validated = {}
    if "pioneer_bonus" in settings_dict:
        val = Decimal(str(settings_dict["pioneer_bonus"]))
        if not (PIONEER_BONUS_MIN <= val <= PIONEER_BONUS_MAX):
            raise BadRequest(
                f"pioneer_bonus must be between {PIONEER_BONUS_MIN} and {PIONEER_BONUS_MAX}"
            )
        validated["pioneer_bonus"] = str(val)
    if "decay_rate" in settings_dict:
        val = Decimal(str(settings_dict["decay_rate"]))
        if not (PIONEER_DECAY_MIN <= val <= PIONEER_DECAY_MAX):
            raise BadRequest(
                f"decay_rate must be between {PIONEER_DECAY_MIN} and {PIONEER_DECAY_MAX}"
            )
        validated["decay_rate"] = str(val)
    return validated


def create_project(founder, data) -> Project:
    """Create a new project proposal. Founder must be TRUSTED+."""
    if founder.trust_level < TrustLevel.TRUSTED:
        raise PermissionDenied("Must be trust level TRUSTED or higher to create a project")

    project = Project.objects.create(
        title=data.title,
        slug=data.slug,
        one_liner=data.one_liner,
        problem=data.problem,
        solution=data.solution,
        target_user=data.target_user,
        revenue_model=data.revenue_model,
        tech_stack_tags=data.tech_stack_tags,
        founder=founder,
        proposal_ends_at=timezone.now() + timedelta(hours=PROPOSAL_BUFFER_HOURS),
    )

    ProjectMember.objects.create(
        project=project,
        user=founder,
        is_seed_team=True,
    )

    publish_project_event(
        project.id,
        "project.created",
        {"project_id": project.id, "founder_id": founder.id, "slug": project.slug},
    )

    return project


def update_project(project: Project, user, data) -> Project:
    """Only founder can update project fields."""
    if project.founder_id != user.id:
        raise PermissionDenied("Only the project founder can update the project")

    update_fields = []
    for field, value in data.dict(exclude_unset=True).items():
        if field == "settings":
            validated = validate_project_settings(value)
            merged = {**project.settings, **validated}
            project.settings = merged
            update_fields.append("settings")
        else:
            setattr(project, field, value)
            update_fields.append(field)

    if update_fields:
        project.save(update_fields=update_fields + ["updated_at"])

    return project


def transition_lifecycle(project: Project, user, target_stage: str) -> Project:
    """Transition project lifecycle stage with validation."""
    if project.founder_id != user.id:
        raise PermissionDenied("Only the project founder can transition lifecycle stages")

    current = project.lifecycle_stage
    allowed = LIFECYCLE_TRANSITIONS.get(current, [])
    if target_stage not in allowed:
        raise InvalidStateTransition(current, target_stage)

    now = timezone.now()
    project.lifecycle_stage = target_stage

    if target_stage == LifecycleStage.INCUBATION:
        project.incubation_started_at = now
    elif target_stage == LifecycleStage.ACTIVE_BUILD:
        project.active_build_started_at = now
    elif target_stage == LifecycleStage.SHIPPED:
        project.shipped_at = now
    elif target_stage == LifecycleStage.SUNSET:
        project.sunset_at = now

    project.save(update_fields=["lifecycle_stage", "updated_at",
                                 "incubation_started_at", "active_build_started_at",
                                 "shipped_at", "sunset_at"])

    publish_project_event(
        project.id,
        "project.lifecycle_transitioned",
        {"project_id": project.id, "from_stage": current, "to_stage": target_stage},
    )

    return project


def add_member(project: Project, user, is_seed_team: bool = False) -> ProjectMember:
    """Add a member to the project."""
    stage = project.lifecycle_stage

    # During incubation, only founder can add seed team
    if stage == LifecycleStage.INCUBATION:
        if is_seed_team and user.id == project.founder_id:
            pass  # founder adding seed team during incubation is allowed
        elif is_seed_team:
            raise PermissionDenied("Only the founder can add seed team members during incubation")
    elif stage == LifecycleStage.PROPOSAL:
        raise BadRequest("Cannot add members during proposal stage")

    # AI agents excluded from seed team
    if is_seed_team and user.is_ai_agent:
        raise BadRequest("AI agents cannot be seed team members")

    # From active_build onward, open membership
    if stage in (LifecycleStage.ACTIVE_BUILD, LifecycleStage.SHIPPED,
                 LifecycleStage.EARNING):
        pass  # open membership

    if ProjectMember.objects.filter(project=project, user=user, removed_at__isnull=True).exists():
        raise Conflict("User is already a member of this project")

    member = ProjectMember.objects.create(
        project=project,
        user=user,
        is_seed_team=is_seed_team,
    )

    publish_project_event(
        project.id,
        "project.member_added",
        {"project_id": project.id, "user_id": user.id, "is_seed_team": is_seed_team},
    )

    return member


def remove_member(project: Project, requester, member_user) -> None:
    """Remove a member from the project. Only founder can remove."""
    if project.founder_id != requester.id:
        raise PermissionDenied("Only the project founder can remove members")

    if member_user.id == requester.id:
        raise BadRequest("Cannot remove yourself from the project")

    member = ProjectMember.objects.filter(
        project=project, user=member_user, removed_at__isnull=True
    ).first()
    if not member:
        raise NotFound("Member not found")

    member.removed_at = timezone.now()
    member.save(update_fields=["removed_at"])

    publish_project_event(
        project.id,
        "project.member_removed",
        {"project_id": project.id, "user_id": member_user.id},
    )


def get_project(slug: str) -> Project:
    """Lookup project by slug."""
    project = Project.objects.filter(slug=slug).first()
    if not project:
        raise NotFound("Project not found")
    return project


def list_projects(lifecycle_stage: str | None = None) -> QuerySet:
    """List projects with optional lifecycle_stage filter."""
    qs = Project.objects.all().order_by("-created_at")
    if lifecycle_stage:
        qs = qs.filter(lifecycle_stage=lifecycle_stage)
    return qs
