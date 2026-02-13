from django.contrib.auth import login
from django.middleware.csrf import get_token
from ninja import Router

from core.permissions import require_auth, require_human, require_trust_level
from core.constants import TrustLevel

from .models import User
from .schemas import (
    AddVerificationIn,
    LoginIn,
    RegisterAgentIn,
    RegisterIn,
    TokenOut,
    TrustProgressOut,
    UserOut,
    UserProfileOut,
    VerificationOut,
    VouchIn,
    VouchOut,
)
from . import services

router = Router()


@router.post("/register", response=TokenOut)
def register(request, payload: RegisterIn):
    user = services.register_user(payload.username, payload.email, payload.password)
    login(request, user)
    return {"token": get_token(request)}


@router.post("/login", response=TokenOut)
def login_view(request, payload: LoginIn):
    user = services.authenticate_user(payload.username, payload.password)
    login(request, user)
    return {"token": get_token(request)}


@router.get("/me", response=UserProfileOut)
@require_auth
def me(request):
    user = request.user
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "identity_score": user.identity_score,
        "trust_level": user.trust_level,
        "is_ai_agent": user.is_ai_agent,
        "date_joined": user.date_joined,
        "verification_count": user.verifications.filter(revoked_at__isnull=True).count(),
        "vouch_count": user.vouches_received.filter(revoked_at__isnull=True).count(),
    }


@router.put("/me", response=UserOut)
@require_auth
def update_me(request, payload: UserOut):
    user = request.user
    user.username = payload.username
    user.email = payload.email
    user.save(update_fields=["username", "email"])
    return user


@router.post("/agents", response=UserOut)
@require_auth
@require_human
def create_agent(request, payload: RegisterAgentIn):
    return services.register_ai_agent(request.user, payload.username)


@router.get("/agents", response=list[UserOut])
@require_auth
def list_agents(request):
    return services.list_user_agents(request.user)


@router.post("/verifications", response=VerificationOut)
@require_auth
def add_verification(request, payload: AddVerificationIn):
    return services.add_verification(
        request.user, payload.method, payload.provider_user_id, payload.metadata
    )


@router.get("/verifications", response=list[VerificationOut])
@require_auth
def list_verifications(request):
    return request.user.verifications.filter(revoked_at__isnull=True)


@router.get("/trust-progress", response=TrustProgressOut)
@require_auth
def trust_progress(request):
    return services.get_trust_progress(request.user)


@router.post("/vouch", response=VouchOut)
@require_trust_level(TrustLevel.TRUSTED)
def vouch(request, payload: VouchIn):
    from core.exceptions import NotFound

    vouchee = User.objects.filter(id=payload.vouchee_id).first()
    if not vouchee:
        raise NotFound("User not found")
    return services.vouch_for_user(request.user, vouchee)
