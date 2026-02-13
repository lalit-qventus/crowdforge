from uuid import UUID

from ninja import Router

from core.permissions import require_auth

from .models import KarmaLedger
from .schemas import KarmaBalanceOut, KarmaLedgerOut
from . import services

router = Router()


@router.get("/{project_id}/balance", response=KarmaBalanceOut)
@require_auth
def get_balance(request, project_id: UUID):
    from apps.projects.models import Project
    from core.exceptions import NotFound

    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise NotFound("Project not found")
    return services.get_balance(project, request.user)


@router.get("/{project_id}/leaderboard", response=list[KarmaBalanceOut])
def get_leaderboard(request, project_id: UUID):
    from apps.projects.models import Project
    from core.exceptions import NotFound

    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise NotFound("Project not found")
    return services.get_project_leaderboard(project)


@router.get("/{project_id}/ledger", response=list[KarmaLedgerOut])
@require_auth
def get_ledger(request, project_id: UUID, cursor: str = None, limit: int = 50):
    qs = KarmaLedger.objects.filter(
        project_id=project_id, user=request.user
    ).order_by("created_at")

    if cursor:
        qs = qs.filter(created_at__gt=cursor)

    return qs[:limit]
