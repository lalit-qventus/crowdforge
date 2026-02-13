from functools import wraps

from django.http import HttpRequest

from core.constants import TrustLevel, REVIEWER_MIN_PROJECT_KARMA
from core.exceptions import PermissionDenied, InsufficientTrustLevel, InsufficientKarma


def require_auth(func):
    """Ensure the request has an authenticated user."""
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        return func(request, *args, **kwargs)
    return wrapper


def require_trust_level(min_level: TrustLevel):
    """Ensure the authenticated user meets a minimum trust level."""
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("Authentication required")
            if request.user.trust_level < min_level:
                raise InsufficientTrustLevel(min_level)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_human(func):
    """Block AI agents from this endpoint."""
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            raise PermissionDenied("Authentication required")
        if request.user.is_ai_agent:
            raise PermissionDenied("This action is restricted to human users")
        return func(request, *args, **kwargs)
    return wrapper


def require_project_karma(min_karma=REVIEWER_MIN_PROJECT_KARMA):
    """Ensure the user has sufficient karma in the specified project."""
    def decorator(func):
        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            from apps.karma.models import KarmaBalance

            project_id = kwargs.get("project_id")
            if not project_id:
                raise PermissionDenied("Project context required")

            balance = KarmaBalance.objects.filter(
                project_id=project_id, user=request.user
            ).first()

            current_karma = balance.total_karma if balance else 0
            if current_karma < min_karma:
                raise InsufficientKarma(min_karma)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
