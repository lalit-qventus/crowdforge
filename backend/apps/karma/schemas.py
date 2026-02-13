from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema


class KarmaLedgerOut(Schema):
    id: UUID
    event_type: str
    amount: Decimal
    balance_after: Decimal
    formula_inputs: dict
    contribution_id: UUID | None
    description: str
    created_at: datetime


class KarmaBalanceOut(Schema):
    project_id: UUID
    user_id: UUID
    total_karma: Decimal
    vested_karma: Decimal
    contribution_count: int
    last_contribution_at: datetime | None


class TopContributorOut(Schema):
    user_id: UUID
    total_karma: Decimal


class ProjectKarmaSummaryOut(Schema):
    project_id: UUID
    total_karma_issued: Decimal
    unique_contributors: int
    top_contributors: list[TopContributorOut]
