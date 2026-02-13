from uuid import UUID

from django.http import HttpRequest
from ninja import Router

from apps.accounts.models import User
from core.constants import TrustLevel
from core.exceptions import NotFound
from core.permissions import require_auth, require_trust_level

from . import services
from .schemas import (
    AddMemberIn,
    MemberOut,
    ProjectCreateIn,
    ProjectListOut,
    ProjectOut,
    ProjectUpdateIn,
    TransitionIn,
)

router = Router(tags=["projects"])


@router.post("/", response=ProjectOut)
@require_trust_level(TrustLevel.TRUSTED)
def create_project(request: HttpRequest, payload: ProjectCreateIn):
    return services.create_project(request.user, payload)


@router.get("/", response=list[ProjectListOut])
def list_projects(request: HttpRequest, lifecycle_stage: str | None = None):
    return services.list_projects(lifecycle_stage=lifecycle_stage)


@router.get("/{slug}", response=ProjectOut)
def get_project(request: HttpRequest, slug: str):
    return services.get_project(slug)


@router.put("/{slug}", response=ProjectOut)
@require_auth
def update_project(request: HttpRequest, slug: str, payload: ProjectUpdateIn):
    project = services.get_project(slug)
    return services.update_project(project, request.user, payload)


@router.post("/{slug}/transition", response=ProjectOut)
@require_auth
def transition_lifecycle(request: HttpRequest, slug: str, payload: TransitionIn):
    project = services.get_project(slug)
    return services.transition_lifecycle(project, request.user, payload.target_stage)


@router.post("/{slug}/members", response=MemberOut)
@require_auth
def add_member(request: HttpRequest, slug: str, payload: AddMemberIn):
    project = services.get_project(slug)
    member_user = User.objects.filter(id=payload.user_id).first()
    if not member_user:
        raise NotFound("User not found")
    return services.add_member(project, member_user, is_seed_team=payload.is_seed_team)


@router.get("/{slug}/members", response=list[MemberOut])
def list_members(request: HttpRequest, slug: str):
    project = services.get_project(slug)
    return project.members.filter(removed_at__isnull=True)


@router.delete("/{slug}/members/{user_id}", response={204: None})
@require_auth
def remove_member(request: HttpRequest, slug: str, user_id: UUID):
    project = services.get_project(slug)
    member_user = User.objects.filter(id=user_id).first()
    if not member_user:
        raise NotFound("User not found")
    services.remove_member(project, request.user, member_user)
    return 204, None
