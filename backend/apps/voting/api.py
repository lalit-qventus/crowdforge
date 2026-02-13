from uuid import UUID

from ninja import Router

from core.exceptions import NotFound
from core.permissions import require_auth, require_human

from apps.projects.models import Project

from .schemas import CastVoteIn, IdeaRingResultOut, VoteOut
from . import services

router = Router()


@router.post("/vote", response=VoteOut)
@require_auth
@require_human
def cast_vote(request, payload: CastVoteIn):
    return services.cast_vote(request.user, payload.target_type, payload.target_id)


@router.get("/idea-ring/{project_id}", response=IdeaRingResultOut)
def get_idea_ring_status(request, project_id: UUID):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise NotFound("Project not found")
    return services.get_idea_ring_status(project)


@router.get("/contribution/{contribution_id}/upvotes")
def get_contribution_upvotes(request, contribution_id: UUID):
    count = services.get_contribution_upvote_count(contribution_id)
    return {"count": count}
