import time

from django.core.cache import cache
from django.http import JsonResponse

from core.constants import TrustLevel


class RateLimitMiddleware:
    """Trust-level-aware rate limiting backed by Redis."""

    RATE_LIMITS = {
        TrustLevel.OBSERVER: (60, 60),       # 60 requests/minute
        TrustLevel.PARTICIPANT: (120, 60),
        TrustLevel.CONTRIBUTOR: (200, 60),
        TrustLevel.TRUSTED: (300, 60),
        TrustLevel.STEWARD: (500, 60),
    }

    DEFAULT_LIMIT = (60, 60)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.path.startswith("/api/"):
            return self.get_response(request)

        if request.user.is_authenticated:
            key = f"ratelimit:user:{request.user.pk}"
            trust = TrustLevel(request.user.trust_level)
            max_requests, window = self.RATE_LIMITS.get(trust, self.DEFAULT_LIMIT)
        else:
            ip = self._get_client_ip(request)
            key = f"ratelimit:anon:{ip}"
            max_requests, window = self.DEFAULT_LIMIT

        current = cache.get(key, 0)
        if current >= max_requests:
            return JsonResponse(
                {"detail": "Rate limit exceeded"},
                status=429,
            )

        pipe_key = f"{key}:set"
        if cache.get(pipe_key) is None:
            cache.set(key, 1, timeout=window)
            cache.set(pipe_key, 1, timeout=window)
        else:
            cache.incr(key)

        return self.get_response(request)

    @staticmethod
    def _get_client_ip(request):
        forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded:
            return forwarded.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
