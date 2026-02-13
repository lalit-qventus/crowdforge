from decimal import Decimal

import pytest

from apps.karma.formulas import contribution_karma, pioneer_multiplier, upvote_score


class TestPioneerMultiplier:
    def test_day_zero(self):
        result = pioneer_multiplier(0)
        assert result == Decimal("3.0")

    def test_day_30(self):
        result = pioneer_multiplier(30)
        # 1 + 2 * e^(-0.3) ~ 2.4816
        assert Decimal("2.47") < result < Decimal("2.49")

    def test_day_90(self):
        result = pioneer_multiplier(90)
        # 1 + 2 * e^(-0.9) ~ 1.8131
        assert Decimal("1.80") < result < Decimal("1.82")

    def test_day_180(self):
        result = pioneer_multiplier(180)
        # 1 + 2 * e^(-1.8) ~ 1.3306
        assert Decimal("1.32") < result < Decimal("1.34")

    def test_day_365(self):
        result = pioneer_multiplier(365)
        # 1 + 2 * e^(-3.65) ~ 1.0522
        assert Decimal("1.04") < result < Decimal("1.06")

    def test_custom_bonus(self):
        result = pioneer_multiplier(0, bonus=Decimal("3.0"))
        assert result == Decimal("4.0")

    def test_custom_decay(self):
        result = pioneer_multiplier(100, decay=Decimal("0.05"))
        # e^(-5) ~ 0.0067, so 1 + 2*0.0067 ~ 1.013
        assert Decimal("1.01") < result < Decimal("1.02")

    def test_large_days_approaches_one(self):
        result = pioneer_multiplier(1000)
        assert Decimal("1.0") < result < Decimal("1.001")


class TestUpvoteScore:
    def test_zero_votes(self):
        assert upvote_score(0) == Decimal("0")

    def test_negative_votes(self):
        assert upvote_score(-5) == Decimal("0")

    def test_one_vote(self):
        result = upvote_score(1)
        assert Decimal("0.29") < result < Decimal("0.31")

    def test_nine_votes(self):
        result = upvote_score(9)
        assert Decimal("0.99") < result < Decimal("1.01")

    def test_ninety_nine_votes(self):
        result = upvote_score(99)
        assert Decimal("1.99") < result < Decimal("2.01")

    def test_monotonically_increasing(self):
        prev = upvote_score(0)
        for count in [1, 5, 10, 50, 100]:
            current = upvote_score(count)
            assert current > prev
            prev = current


class TestContributionKarma:
    def test_basic_calculation(self):
        result = contribution_karma(
            base=Decimal("10"),
            pioneer=Decimal("2.0"),
            upvote=Decimal("0.5"),
        )
        # 10 * 2.0 * (1 + 0.5) * 1.0 = 30.0
        assert result == Decimal("30.0")

    def test_with_ai_multiplier(self):
        result = contribution_karma(
            base=Decimal("10"),
            pioneer=Decimal("2.0"),
            upvote=Decimal("0.5"),
            ai_multiplier=Decimal("0.7"),
        )
        # 10 * 2.0 * 1.5 * 0.7 = 21.0
        assert result == Decimal("21.0")

    def test_zero_upvotes(self):
        result = contribution_karma(
            base=Decimal("10"),
            pioneer=Decimal("1.5"),
            upvote=Decimal("0"),
        )
        # 10 * 1.5 * 1.0 * 1.0 = 15.0
        assert result == Decimal("15.0")

    def test_high_upvotes(self):
        result = contribution_karma(
            base=Decimal("10"),
            pioneer=Decimal("1.0"),
            upvote=Decimal("2.0"),
        )
        # 10 * 1.0 * 3.0 * 1.0 = 30.0
        assert result == Decimal("30.0")

    def test_different_base_values(self):
        for base_val in [Decimal("5"), Decimal("8"), Decimal("10")]:
            result = contribution_karma(
                base=base_val,
                pioneer=Decimal("1.0"),
                upvote=Decimal("0"),
            )
            assert result == base_val

    def test_ai_multiplier_reduces_karma(self):
        human_karma = contribution_karma(
            base=Decimal("10"),
            pioneer=Decimal("2.0"),
            upvote=Decimal("1.0"),
        )
        ai_karma = contribution_karma(
            base=Decimal("10"),
            pioneer=Decimal("2.0"),
            upvote=Decimal("1.0"),
            ai_multiplier=Decimal("0.7"),
        )
        assert ai_karma < human_karma
        assert ai_karma == human_karma * Decimal("0.7")
