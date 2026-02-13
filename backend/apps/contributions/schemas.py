from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema


class ContributionCreateIn(Schema):
    project_id: UUID
    title: str
    description: str = ""
    category: str
    task_id: UUID | None = None
    external_pr_url: str = ""
    diff_summary: str = ""


class ContributionUpdateIn(Schema):
    title: str | None = None
    description: str | None = None
    external_pr_url: str | None = None
    diff_summary: str | None = None


class ContributionOut(Schema):
    id: UUID
    project_id: UUID
    author_id: UUID
    task_id: UUID | None
    title: str
    description: str
    category: str
    external_pr_url: str
    diff_summary: str
    status: str
    reviewer_id: UUID | None
    review_note: str
    base_karma: Decimal
    pioneer_multiplier: Decimal
    upvote_score: Decimal
    ai_multiplier: Decimal
    karma_awarded: Decimal
    karma_vested: Decimal
    submitted_at: datetime | None
    accepted_at: datetime | None
    rejected_at: datetime | None
    reverted_at: datetime | None
    reverted_by_id: UUID | None
    created_at: datetime
    updated_at: datetime


class ContributionListOut(Schema):
    id: UUID
    title: str
    category: str
    status: str
    author_id: UUID
    reviewer_id: UUID | None
    karma_awarded: Decimal
    submitted_at: datetime | None
    accepted_at: datetime | None
    created_at: datetime


class SubmitIn(Schema):
    pass


class ReviewIn(Schema):
    action: str
    review_note: str = ""


class RevertIn(Schema):
    reason: str
