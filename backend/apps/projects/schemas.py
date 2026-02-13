from datetime import datetime
from uuid import UUID

from ninja import Schema


class ProjectCreateIn(Schema):
    title: str
    slug: str
    one_liner: str = ""
    problem: str = ""
    solution: str = ""
    target_user: str = ""
    revenue_model: str = ""
    tech_stack_tags: list[str] = []


class ProjectUpdateIn(Schema):
    title: str | None = None
    one_liner: str | None = None
    problem: str | None = None
    solution: str | None = None
    target_user: str | None = None
    revenue_model: str | None = None
    tech_stack_tags: list[str] | None = None
    production_url: str | None = None
    staging_url: str | None = None
    repo_url: str | None = None
    settings: dict | None = None


class ProjectOut(Schema):
    id: UUID
    slug: str
    title: str
    one_liner: str
    problem: str
    solution: str
    target_user: str
    revenue_model: str
    tech_stack_tags: list[str]
    lifecycle_stage: str
    proposal_ends_at: datetime | None
    incubation_started_at: datetime | None
    active_build_started_at: datetime | None
    shipped_at: datetime | None
    sunset_at: datetime | None
    founder_id: UUID
    production_url: str
    staging_url: str
    repo_url: str
    settings: dict
    accepted_contributions: int
    unique_contributors: int
    first_revenue: bool
    milestone_1_reached: bool
    milestone_2_reached: bool
    created_at: datetime
    updated_at: datetime


class ProjectListOut(Schema):
    id: UUID
    slug: str
    title: str
    one_liner: str
    lifecycle_stage: str
    tech_stack_tags: list[str]
    founder_id: UUID
    accepted_contributions: int
    unique_contributors: int
    created_at: datetime


class TransitionIn(Schema):
    target_stage: str


class MemberOut(Schema):
    id: UUID
    user_id: UUID
    is_seed_team: bool
    joined_at: datetime


class AddMemberIn(Schema):
    user_id: UUID
    is_seed_team: bool = False


class ProjectSettingsOut(Schema):
    settings: dict
