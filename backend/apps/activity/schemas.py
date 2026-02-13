from datetime import datetime
from uuid import UUID

from ninja import Schema


class ActivityEventOut(Schema):
    id: UUID
    event_type: str
    actor_username: str
    actor_avatar_url: str
    project_slug: str
    project_title: str
    target_type: str
    target_id: UUID | None
    metadata: dict
    summary: str
    created_at: datetime


class FeedOut(Schema):
    items: list[ActivityEventOut]
    next_cursor: str | None
