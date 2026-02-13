import json
from datetime import datetime
from decimal import Decimal
from uuid import UUID

import redis
from django.conf import settings


class _JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        if isinstance(obj, UUID):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def _get_redis():
    url = getattr(settings, "REDIS_URL", None) or "redis://127.0.0.1:6379/0"
    return redis.from_url(url)


def publish_event(channel: str, event_type: str, data: dict):
    """Publish an event to a Redis pub/sub channel."""
    payload = json.dumps(
        {"event_type": event_type, "data": data},
        cls=_JSONEncoder,
    )
    _get_redis().publish(channel, payload)


def publish_project_event(project_id, event_type: str, data: dict):
    publish_event(f"project:{project_id}", event_type, data)


def publish_user_event(user_id, event_type: str, data: dict):
    publish_event(f"user:{user_id}", event_type, data)
