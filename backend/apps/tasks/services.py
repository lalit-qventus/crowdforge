from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone

from apps.projects.models import ProjectMember
from core.constants import MAX_ACTIVE_TASK_CLAIMS, TASK_CLAIM_HOURS, TASK_EXTEND_HOURS
from core.events import publish_project_event
from core.exceptions import BadRequest, NotFound, PermissionDenied

from .models import Task, TaskStatus


def create_task(project, creator, data) -> Task:
    """Creator must be a project member."""
    if not ProjectMember.objects.filter(
        project=project, user=creator, removed_at__isnull=True
    ).exists():
        raise PermissionDenied("Must be a project member to create tasks")

    task = Task.objects.create(
        project=project,
        creator=creator,
        title=data.title,
        description=data.description,
        acceptance_criteria=data.acceptance_criteria,
        category=data.category,
        estimated_effort=data.estimated_effort,
        required_skills=data.required_skills,
        karma_bounty=data.karma_bounty,
        is_critical=data.is_critical,
    )

    publish_project_event(
        project.id,
        "task.created",
        {"task_id": task.id, "project_id": project.id, "creator_id": creator.id},
    )

    return task


def update_task(task: Task, user, data) -> Task:
    """Only creator or project founder can update. Only open tasks."""
    if task.status != TaskStatus.OPEN:
        raise BadRequest("Can only update open tasks")

    is_creator = task.creator_id == user.id
    is_founder = task.project.founder_id == user.id
    if not (is_creator or is_founder):
        raise PermissionDenied("Only the task creator or project founder can update tasks")

    update_fields = []
    for field, value in data.dict(exclude_unset=True).items():
        setattr(task, field, value)
        update_fields.append(field)

    if update_fields:
        task.save(update_fields=update_fields + ["updated_at"])

    return task


def claim_task(task: Task, user) -> Task:
    """Claim an open task. User must be a project member with < MAX_ACTIVE_TASK_CLAIMS active claims."""
    if task.status != TaskStatus.OPEN:
        raise BadRequest("Task is not open for claiming")

    if not ProjectMember.objects.filter(
        project=task.project, user=user, removed_at__isnull=True
    ).exists():
        raise PermissionDenied("Must be a project member to claim tasks")

    active_claims = Task.objects.filter(
        assignee=user, status__in=[TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS]
    ).count()
    if active_claims >= MAX_ACTIVE_TASK_CLAIMS:
        raise BadRequest(f"Cannot have more than {MAX_ACTIVE_TASK_CLAIMS} active task claims")

    now = timezone.now()
    task.status = TaskStatus.CLAIMED
    task.assignee = user
    task.claimed_at = now
    task.claim_expires_at = now + timedelta(hours=TASK_CLAIM_HOURS)
    task.save(update_fields=[
        "status", "assignee", "claimed_at", "claim_expires_at", "updated_at",
    ])

    publish_project_event(
        task.project_id,
        "task.claimed",
        {"task_id": task.id, "user_id": user.id},
    )

    return task


def extend_claim(task: Task, user) -> Task:
    """Extend a claimed task's deadline. Can only extend once."""
    if task.status != TaskStatus.CLAIMED:
        raise BadRequest("Task must be in claimed status to extend")

    if task.assignee_id != user.id:
        raise PermissionDenied("Only the assignee can extend the claim")

    if task.extended_once:
        raise BadRequest("Claim can only be extended once")

    task.claim_expires_at = task.claim_expires_at + timedelta(hours=TASK_EXTEND_HOURS)
    task.extended_once = True
    task.save(update_fields=["claim_expires_at", "extended_once", "updated_at"])

    return task


def release_task(task: Task, user) -> Task:
    """Release a claimed/in_progress task. Assignee or founder can release."""
    if task.status not in (TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS):
        raise BadRequest("Task must be claimed or in progress to release")

    is_assignee = task.assignee_id == user.id
    is_founder = task.project.founder_id == user.id
    if not (is_assignee or is_founder):
        raise PermissionDenied("Only the assignee or project founder can release tasks")

    task.status = TaskStatus.OPEN
    task.assignee = None
    task.claimed_at = None
    task.claim_expires_at = None
    task.save(update_fields=[
        "status", "assignee", "claimed_at", "claim_expires_at", "updated_at",
    ])

    publish_project_event(
        task.project_id,
        "task.released",
        {"task_id": task.id, "user_id": user.id},
    )

    return task


def complete_task(task: Task, user) -> Task:
    """Complete a task. Must be claimed/in_progress by assignee."""
    if task.status not in (TaskStatus.CLAIMED, TaskStatus.IN_PROGRESS):
        raise BadRequest("Task must be claimed or in progress to complete")

    if task.assignee_id != user.id:
        raise PermissionDenied("Only the assignee can complete the task")

    task.status = TaskStatus.COMPLETED
    task.completed_at = timezone.now()
    task.save(update_fields=["status", "completed_at", "updated_at"])

    publish_project_event(
        task.project_id,
        "task.completed",
        {"task_id": task.id, "user_id": user.id},
    )

    return task


def cancel_task(task: Task, user) -> Task:
    """Cancel a task. Only creator or project founder."""
    is_creator = task.creator_id == user.id
    is_founder = task.project.founder_id == user.id
    if not (is_creator or is_founder):
        raise PermissionDenied("Only the task creator or project founder can cancel tasks")

    task.status = TaskStatus.CANCELLED
    task.save(update_fields=["status", "updated_at"])

    return task


def get_task(task_id) -> Task:
    """Lookup task by ID."""
    task = Task.objects.select_related("project").filter(id=task_id).first()
    if not task:
        raise NotFound("Task not found")
    return task


def list_project_tasks(project, status_filter: str | None = None) -> QuerySet:
    """List tasks for a project with optional status filter."""
    qs = Task.objects.filter(project=project).order_by("-created_at")
    if status_filter:
        qs = qs.filter(status=status_filter)
    return qs
