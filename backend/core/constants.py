from decimal import Decimal
from enum import IntEnum

# --- Karma Base Values (per contribution category) ---
BASE_KARMA = {
    "ideation": Decimal("5"),
    "code": Decimal("10"),
    "design": Decimal("8"),
    "testing": Decimal("7"),
    "marketing": Decimal("6"),
    "sales": Decimal("0"),  # variable — 1 karma per $100 attributed revenue
    "governance": Decimal("4"),
}

# --- Pioneer Multiplier Defaults ---
PIONEER_BONUS_DEFAULT = Decimal("2.0")
PIONEER_DECAY_DEFAULT = Decimal("0.01")

# Pioneer configurable ranges (per-project)
PIONEER_BONUS_MIN = Decimal("1.0")
PIONEER_BONUS_MAX = Decimal("3.0")
PIONEER_DECAY_MIN = Decimal("0.005")
PIONEER_DECAY_MAX = Decimal("0.05")

# --- AI Agent Constraints ---
AI_KARMA_MULTIPLIER_ACTIVE_BUILD = Decimal("0.7")
AI_KARMA_MULTIPLIER_DEFAULT = Decimal("1.0")
AI_MAX_AGENTS_PER_HUMAN = 3
AI_MAX_CONTRIBUTIONS_PER_PROJECT_DAY_ACTIVE = 5
AI_MAX_CONTRIBUTIONS_PER_PROJECT_DAY_GROWTH = 20
AI_MAX_SIMULTANEOUS_ACTIVE_BUILD_PROJECTS = 3

# --- Trust Levels ---
class TrustLevel(IntEnum):
    OBSERVER = 0
    PARTICIPANT = 1
    CONTRIBUTOR = 2
    TRUSTED = 3
    STEWARD = 4


TRUST_LEVEL_REQUIREMENTS = {
    TrustLevel.OBSERVER: {
        "identity_score": 0,
        "account_age_days": 0,
        "accepted_contributions": 0,
    },
    TrustLevel.PARTICIPANT: {
        "identity_score": 20,
        "account_age_days": 7,
        "accepted_contributions": 0,
    },
    TrustLevel.CONTRIBUTOR: {
        "identity_score": 40,
        "account_age_days": 30,
        "accepted_contributions": 1,
    },
    TrustLevel.TRUSTED: {
        "identity_score": 60,
        "account_age_days": 90,
        "accepted_contributions": 5,
        "distinct_projects": 2,
        "distinct_upvoters": 5,
    },
    TrustLevel.STEWARD: {
        "identity_score": 60,
        "account_age_days": 180,
        "accepted_contributions": 20,
    },
}

# --- Identity Verification Scores ---
VERIFICATION_SCORES = {
    "email": 5,
    "phone_sms": 15,
    "phone_sms_voip": 5,
    "social_oauth": 20,
    "social_oauth_new": 10,  # account < 30 days
    "github_history": 30,
    "world_id": 40,
    "vouching": 25,
}

PAYOUT_IDENTITY_THRESHOLD = 40

# --- Rate Limits (contributions per day by trust level) ---
CONTRIBUTION_RATE_LIMITS = {
    TrustLevel.OBSERVER: 0,
    TrustLevel.PARTICIPANT: 3,
    TrustLevel.CONTRIBUTOR: 10,
    TrustLevel.TRUSTED: 25,
    TrustLevel.STEWARD: 25,
}

# --- Voting ---
IDEA_RING_VOTE_WINDOW_HOURS = 72
IDEA_RING_QUORUM = 25
IDEA_RING_THRESHOLD = Decimal("0.60")
FOUNDER_SELF_VOTE_WEIGHT = Decimal("0.5")
SELF_VOTE_WEIGHT = Decimal("0")

# --- Karma Vesting ---
VESTING_IMMEDIATE_PERCENT = Decimal("0.25")
VESTING_LINEAR_DAYS = 90

# --- Revert Penalty ---
REVERT_PENALTY_MULTIPLIER = Decimal("1.20")

# --- Task Constraints ---
MAX_ACTIVE_TASK_CLAIMS = 3
TASK_CLAIM_HOURS = 48
TASK_EXTEND_HOURS = 48

# --- Reviewer Karma Threshold ---
REVIEWER_MIN_PROJECT_KARMA = Decimal("50")

# --- Revenue Distribution ---
# 100% to karma-weighted contributors. Platform earns its share
# through karma (hosting, tooling, infrastructure contributions).
REVENUE_CONTRIBUTOR_POOL = Decimal("1.00")
REVENUE_PLATFORM_FEE = Decimal("0")
REVENUE_PROJECT_TREASURY = Decimal("0")

# --- Lifecycle ---
PROPOSAL_BUFFER_HOURS = 48
