from django.contrib.auth import authenticate
from django.db.models import Sum
from django.utils import timezone

from core.constants import (
    AI_MAX_AGENTS_PER_HUMAN,
    TRUST_LEVEL_REQUIREMENTS,
    TrustLevel,
    VERIFICATION_SCORES,
)
from core.events import publish_user_event
from core.exceptions import BadRequest, Conflict, PermissionDenied

from .models import User, UserVerification, VerificationMethod, Vouch


def register_user(username: str, email: str, password: str) -> User:
    if User.objects.filter(username=username).exists():
        raise Conflict("Username already taken")
    if User.objects.filter(email=email).exists():
        raise Conflict("Email already registered")

    user = User.objects.create_user(username=username, email=email, password=password)

    UserVerification.objects.create(
        user=user,
        method=VerificationMethod.EMAIL,
        score_awarded=VERIFICATION_SCORES["email"],
    )
    user.identity_score = VERIFICATION_SCORES["email"]
    user.save(update_fields=["identity_score"])

    publish_user_event(user.id, "user.registered", {"username": username})
    return user


def authenticate_user(username: str, password: str) -> User:
    user = authenticate(username=username, password=password)
    if user is None:
        raise BadRequest("Invalid credentials")
    return user


def register_ai_agent(parent_user: User, username: str) -> User:
    agent_count = User.objects.filter(parent_user=parent_user).count()
    if agent_count >= AI_MAX_AGENTS_PER_HUMAN:
        raise BadRequest(
            f"Maximum {AI_MAX_AGENTS_PER_HUMAN} AI agents per human user"
        )

    if User.objects.filter(username=username).exists():
        raise Conflict("Username already taken")

    agent = User.objects.create_user(
        username=username,
        password=None,
        is_ai_agent=True,
        parent_user=parent_user,
    )
    return agent


def add_verification(
    user: User, method: str, provider_user_id: str = "", metadata: dict | None = None,
) -> UserVerification:
    if UserVerification.objects.filter(user=user, method=method).exists():
        raise Conflict(f"Verification method '{method}' already exists for this user")

    score = VERIFICATION_SCORES.get(method, 0)

    verification = UserVerification.objects.create(
        user=user,
        method=method,
        provider_user_id=provider_user_id,
        score_awarded=score,
        metadata=metadata or {},
    )

    recompute_identity_score(user)

    publish_user_event(
        user.id, "user.verification_added", {"method": method, "score": score}
    )
    return verification


def recompute_identity_score(user: User) -> int:
    total = (
        UserVerification.objects.filter(user=user, revoked_at__isnull=True).aggregate(
            total=Sum("score_awarded")
        )["total"]
        or 0
    )
    user.identity_score = total
    user.save(update_fields=["identity_score"])
    return total


def evaluate_trust_level(user: User) -> TrustLevel:
    account_age_days = (timezone.now() - user.date_joined).days

    from apps.karma.models import KarmaBalance

    accepted_contributions = KarmaBalance.objects.filter(user=user).aggregate(
        total=Sum("contribution_count")
    )["total"] or 0

    best_level = TrustLevel.OBSERVER
    for level in sorted(TRUST_LEVEL_REQUIREMENTS.keys()):
        reqs = TRUST_LEVEL_REQUIREMENTS[level]
        if user.identity_score < reqs["identity_score"]:
            break
        if account_age_days < reqs["account_age_days"]:
            break
        if accepted_contributions < reqs["accepted_contributions"]:
            break

        # TRUSTED level has extra requirements
        if level == TrustLevel.TRUSTED:
            distinct_projects = (
                KarmaBalance.objects.filter(
                    user=user, contribution_count__gt=0
                ).values("project").distinct().count()
            )
            if distinct_projects < reqs.get("distinct_projects", 0):
                break

            from apps.karma.models import KarmaLedger

            distinct_upvoters = (
                KarmaLedger.objects.filter(user=user)
                .values("contribution__votes__voter")
                .distinct()
                .count()
            )
            if distinct_upvoters < reqs.get("distinct_upvoters", 0):
                break

        best_level = level

    user.trust_level = best_level
    user.save(update_fields=["trust_level"])
    return TrustLevel(best_level)


def get_trust_progress(user: User) -> dict:
    account_age_days = (timezone.now() - user.date_joined).days

    from apps.karma.models import KarmaBalance

    accepted_contributions = KarmaBalance.objects.filter(user=user).aggregate(
        total=Sum("contribution_count")
    )["total"] or 0

    current_level = user.trust_level
    next_level = current_level + 1

    next_level_requirements = {}
    if next_level in TRUST_LEVEL_REQUIREMENTS:
        next_level_requirements = TRUST_LEVEL_REQUIREMENTS[TrustLevel(next_level)]

    return {
        "current_level": current_level,
        "identity_score": user.identity_score,
        "account_age_days": account_age_days,
        "accepted_contributions": accepted_contributions,
        "next_level_requirements": next_level_requirements,
    }


def vouch_for_user(voucher: User, vouchee: User) -> Vouch:
    if voucher.trust_level < TrustLevel.TRUSTED:
        raise PermissionDenied("Must be TRUSTED or higher to vouch")
    if voucher == vouchee:
        raise BadRequest("Cannot vouch for yourself")
    if Vouch.objects.filter(voucher=voucher, vouchee=vouchee).exists():
        raise Conflict("Already vouched for this user")

    vouch = Vouch.objects.create(voucher=voucher, vouchee=vouchee)

    active_vouches = Vouch.objects.filter(
        vouchee=vouchee, revoked_at__isnull=True
    ).count()
    if active_vouches >= 2:
        if not UserVerification.objects.filter(
            user=vouchee, method=VerificationMethod.VOUCHING
        ).exists():
            add_verification(vouchee, VerificationMethod.VOUCHING)

    return vouch


def list_user_agents(user: User):
    return User.objects.filter(parent_user=user)
