from datetime import datetime
from decimal import Decimal
from uuid import UUID

from ninja import Schema


class CastVoteIn(Schema):
    target_type: str
    target_id: UUID


class VoteOut(Schema):
    id: UUID
    voter_id: UUID
    target_type: str
    target_id: UUID
    weight: Decimal
    created_at: datetime


class IdeaRingResultOut(Schema):
    project_id: UUID
    total_votes: int
    weighted_score: Decimal
    quorum_met: bool
    threshold_met: bool
    vote_count: int
