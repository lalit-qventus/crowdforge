from datetime import datetime

from django.utils import timezone

from core.events import publish_project_event, publish_user_event

from .models import ActivityEvent


def record_event(
    event_type,
    actor,
    project=None,
    target_type="",
    target_id=None,
    metadata=None,
    summary="",
) -> ActivityEvent:
    event = ActivityEvent.objects.create(
        event_type=event_type,
        actor=actor,
        project=project,
        target_type=target_type,
        target_id=target_id,
        metadata=metadata or {},
        actor_username=actor.username,
        actor_avatar_url="",
        project_slug=project.slug if project else "",
        project_title=project.title if project else "",
        summary=summary,
    )

    if project:
        publish_project_event(
            project.id,
            event_type,
            {"event_id": str(event.id), "actor": actor.username, "summary": summary},
        )
    else:
        publish_user_event(
            actor.id,
            event_type,
            {"event_id": str(event.id), "actor": actor.username, "summary": summary},
        )

    return event


def get_global_feed(cursor=None, limit=20):
    qs = ActivityEvent.objects.all().order_by("-created_at")

    if cursor:
        cursor_dt = datetime.fromisoformat(cursor)
        if timezone.is_naive(cursor_dt):
            cursor_dt = timezone.make_aware(cursor_dt)
        qs = qs.filter(created_at__lt=cursor_dt)

    events = list(qs[:limit + 1])
    next_cursor = None
    if len(events) > limit:
        events = events[:limit]
        next_cursor = events[-1].created_at.isoformat()

    return events, next_cursor


def get_project_feed(project, cursor=None, limit=20):
    qs = ActivityEvent.objects.filter(project=project).order_by("-created_at")

    if cursor:
        cursor_dt = datetime.fromisoformat(cursor)
        if timezone.is_naive(cursor_dt):
            cursor_dt = timezone.make_aware(cursor_dt)
        qs = qs.filter(created_at__lt=cursor_dt)

    events = list(qs[:limit + 1])
    next_cursor = None
    if len(events) > limit:
        events = events[:limit]
        next_cursor = events[-1].created_at.isoformat()

    return events, next_cursor


def get_user_feed(user, cursor=None, limit=20):
    qs = ActivityEvent.objects.filter(actor=user).order_by("-created_at")

    if cursor:
        cursor_dt = datetime.fromisoformat(cursor)
        if timezone.is_naive(cursor_dt):
            cursor_dt = timezone.make_aware(cursor_dt)
        qs = qs.filter(created_at__lt=cursor_dt)

    events = list(qs[:limit + 1])
    next_cursor = None
    if len(events) > limit:
        events = events[:limit]
        next_cursor = events[-1].created_at.isoformat()

    return events, next_cursor
