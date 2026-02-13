from ninja.errors import HttpError


class PermissionDenied(HttpError):
    def __init__(self, message: str = "Permission denied"):
        super().__init__(403, message)


class NotFound(HttpError):
    def __init__(self, message: str = "Not found"):
        super().__init__(404, message)


class BadRequest(HttpError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(400, message)


class Conflict(HttpError):
    def __init__(self, message: str = "Conflict"):
        super().__init__(409, message)


class RateLimited(HttpError):
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(429, message)


class InsufficientTrustLevel(PermissionDenied):
    def __init__(self, required_level: int):
        super().__init__(f"Requires trust level {required_level} or higher")


class InsufficientKarma(PermissionDenied):
    def __init__(self, required_karma):
        super().__init__(f"Requires at least {required_karma} project karma")


class InvalidStateTransition(BadRequest):
    def __init__(self, current_state: str, target_state: str):
        super().__init__(f"Cannot transition from '{current_state}' to '{target_state}'")


class AppendOnlyViolation(BadRequest):
    def __init__(self):
        super().__init__("Karma ledger is append-only; updates and deletes are not allowed")
