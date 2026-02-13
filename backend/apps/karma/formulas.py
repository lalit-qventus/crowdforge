import math
from decimal import Decimal


def pioneer_multiplier(
    days_since_start: int,
    bonus: Decimal = Decimal("2.0"),
    decay: Decimal = Decimal("0.01"),
) -> Decimal:
    """M(t) = 1 + bonus * e^(-decay * t)"""
    return Decimal("1") + bonus * Decimal(
        str(math.exp(float(-decay * days_since_start)))
    )


def upvote_score(count: int) -> Decimal:
    """upvote_score = ln(1 + count) / ln(10)"""
    if count <= 0:
        return Decimal("0")
    return Decimal(str(math.log(1 + count) / math.log(10)))


def contribution_karma(
    base: Decimal,
    pioneer: Decimal,
    upvote: Decimal,
    ai_multiplier: Decimal = Decimal("1.0"),
) -> Decimal:
    """total = base * pioneer * (1 + upvote) * ai_multiplier"""
    return base * pioneer * (Decimal("1") + upvote) * ai_multiplier
