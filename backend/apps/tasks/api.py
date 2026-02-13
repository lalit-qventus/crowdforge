from uuid import UUID

from django.http import HttpRequest
from ninja import Router

from apps.projects.models import Project
from core.exceptions import NotFound
from core.permissions import require_auth

from . import services
from .schemas import TaskCreateIn, TaskListOut, TaskOut, TaskUpdateIn

router = Router(tags=["tasks"])


@router.post("/{project_id}/tasks", response=TaskOut)
@require_auth
def create_task(request: HttpRequest, project_id: UUID, payload: TaskCreateIn):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise NotFound("Project not found")
    return services.create_task(project, request.user, payload)


@router.get("/{project_id}/tasks", response=list[TaskListOut])
def list_tasks(request: HttpRequest, project_id: UUID, status: str | None = None):
    project = Project.objects.filter(id=project_id).first()
    if not project:
        raise NotFound("Project not found")
    return services.list_project_tasks(project, status_filter=status)


@router.get("/tasks/{task_id}", response=TaskOut)
def get_task(request: HttpRequest, task_id: UUID):
    return services.get_task(task_id)


@router.put("/tasks/{task_id}", response=TaskOut)
@require_auth
def update_task(request: HttpRequest, task_id: UUID, payload: TaskUpdateIn):
    task = services.get_task(task_id)
    return services.update_task(task, request.user, payload)


@router.post("/tasks/{task_id}/claim", response=TaskOut)
@require_auth
def claim_task(request: HttpRequest, task_id: UUID):
    task = services.get_task(task_id)
    return services.claim_task(task, request.user)


@router.post("/tasks/{task_id}/extend", response=TaskOut)
@require_auth
def extend_claim(request: HttpRequest, task_id: UUID):
    task = services.get_task(task_id)
    return services.extend_claim(task, request.user)


@router.post("/tasks/{task_id}/release", response=TaskOut)
@require_auth
def release_task(request: HttpRequest, task_id: UUID):
    task = services.get_task(task_id)
    return services.release_task(task, request.user)


@router.post("/tasks/{task_id}/complete", response=TaskOut)
@require_auth
def complete_task(request: HttpRequest, task_id: UUID):
    task = services.get_task(task_id)
    return services.complete_task(task, request.user)


@router.delete("/tasks/{task_id}", response={204: None})
@require_auth
def cancel_task(request: HttpRequest, task_id: UUID):
    task = services.get_task(task_id)
    services.cancel_task(task, request.user)
    return 204, None
