from datetime import datetime
from uuid import UUID

from ninja import Schema


class RegisterIn(Schema):
    username: str
    email: str
    password: str


class LoginIn(Schema):
    username: str
    password: str


class UserOut(Schema):
    id: UUID
    username: str
    email: str
    identity_score: int
    trust_level: int
    is_ai_agent: bool
    date_joined: datetime


class UserProfileOut(UserOut):
    verification_count: int
    vouch_count: int


class RegisterAgentIn(Schema):
    username: str


class AddVerificationIn(Schema):
    method: str
    provider_user_id: str = ""
    metadata: dict = {}


class VerificationOut(Schema):
    id: UUID
    method: str
    score_awarded: int
    verified_at: datetime
    expires_at: datetime | None


class TrustProgressOut(Schema):
    current_level: int
    identity_score: int
    account_age_days: int
    accepted_contributions: int
    next_level_requirements: dict


class VouchIn(Schema):
    vouchee_id: UUID


class VouchOut(Schema):
    id: UUID
    voucher_id: UUID
    vouchee_id: UUID
    created_at: datetime


class TokenOut(Schema):
    token: str
