from uuid import UUID

from ninja import Router

from core.exceptions import NotFound
from core.permissions import require_auth

from .models import Contribution
from .schemas import (
    ContributionCreateIn,
    ContributionListOut,
    ContributionOut,
    ContributionUpdateIn,
    ReviewIn,
    RevertIn,
    SubmitIn,
)
from . import services

router = Router()


@router.post("/", response=ContributionOut)
@require_auth
def create_contribution(request, payload: ContributionCreateIn):
    return services.create_contribution(request.user, payload)


@router.get("/", response=list[ContributionListOut])
def list_contributions(request, project_id: UUID = None):
    qs = Contribution.objects.all()
    if project_id:
        qs = qs.filter(project_id=project_id)
    return qs.order_by("-created_at")


@router.get("/{contribution_id}", response=ContributionOut)
def get_contribution(request, contribution_id: UUID):
    contribution = Contribution.objects.filter(id=contribution_id).first()
    if not contribution:
        raise NotFound("Contribution not found")
    return contribution


@router.put("/{contribution_id}", response=ContributionOut)
@require_auth
def update_contribution(request, contribution_id: UUID, payload: ContributionUpdateIn):
    contribution = Contribution.objects.filter(id=contribution_id).first()
    if not contribution:
        raise NotFound("Contribution not found")
    return services.update_contribution(contribution, request.user, payload)


@router.post("/{contribution_id}/submit", response=ContributionOut)
@require_auth
def submit_contribution(request, contribution_id: UUID):
    contribution = Contribution.objects.filter(id=contribution_id).first()
    if not contribution:
        raise NotFound("Contribution not found")
    return services.submit_contribution(contribution, request.user)


@router.post("/{contribution_id}/review", response=ContributionOut)
@require_auth
def start_review(request, contribution_id: UUID):
    contribution = Contribution.objects.filter(id=contribution_id).first()
    if not contribution:
        raise NotFound("Contribution not found")
    return services.start_review(contribution, request.user)


@router.post("/{contribution_id}/decide", response=ContributionOut)
@require_auth
def decide_contribution(request, contribution_id: UUID, payload: ReviewIn):
    contribution = Contribution.objects.filter(id=contribution_id).first()
    if not contribution:
        raise NotFound("Contribution not found")
    return services.review_contribution(
        contribution, request.user, payload.action, payload.review_note
    )


@router.post("/{contribution_id}/revert", response=ContributionOut)
@require_auth
def revert_contribution(request, contribution_id: UUID, payload: RevertIn):
    contribution = Contribution.objects.filter(id=contribution_id).first()
    if not contribution:
        raise NotFound("Contribution not found")
    return services.revert_contribution(contribution, request.user, payload.reason)
