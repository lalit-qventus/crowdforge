from uuid import UUID

from ninja import Router

from core.exceptions import NotFound

from apps.accounts.models import User
from apps.projects.models import Project

from .schemas import FeedOut
from . import services

router = Router()


@router.get("/feed", response=FeedOut)
def global_feed(request, cursor: str = None, limit: int = 20):
    events, next_cursor = services.get_global_feed(cursor=cursor, limit=limit)
    return {"items": events, "next_cursor": next_cursor}


@router.get("/feed/project/{project_id}", response=FeedOut)
def project_feed(request, project_id: UUID, cursor: str = None, limit: int = 20):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise NotFound("Project not found")
    events, next_cursor = services.get_project_feed(project, cursor=cursor, limit=limit)
    return {"items": events, "next_cursor": next_cursor}


@router.get("/feed/user/{user_id}", response=FeedOut)
def user_feed(request, user_id: UUID, cursor: str = None, limit: int = 20):
    user = User.objects.filter(id=user_id).first()
    if not user:
        raise NotFound("User not found")
    events, next_cursor = services.get_user_feed(user, cursor=cursor, limit=limit)
    return {"items": events, "next_cursor": next_cursor}
