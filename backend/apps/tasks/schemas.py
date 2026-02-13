from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema


class TaskCreateIn(Schema):
    title: str
    description: str = ""
    acceptance_criteria: str = ""
    category: str
    estimated_effort: str = "M"
    required_skills: list[str] = []
    karma_bounty: Decimal = Decimal("0")
    is_critical: bool = False


class TaskUpdateIn(Schema):
    title: str | None = None
    description: str | None = None
    acceptance_criteria: str | None = None
    category: str | None = None
    estimated_effort: str | None = None
    required_skills: list[str] | None = None
    karma_bounty: Decimal | None = None
    is_critical: bool | None = None


class TaskOut(Schema):
    id: UUID
    project_id: UUID
    creator_id: UUID
    title: str
    description: str
    acceptance_criteria: str
    category: str
    estimated_effort: str
    required_skills: list[str]
    karma_bounty: Decimal
    is_critical: bool
    status: str
    assignee_id: UUID | None
    claimed_at: datetime | None
    claim_expires_at: datetime | None
    extended_once: bool
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime


class TaskListOut(Schema):
    id: UUID
    title: str
    category: str
    estimated_effort: str
    status: str
    assignee_id: UUID | None
    karma_bounty: Decimal
    is_critical: bool
    created_at: datetime
