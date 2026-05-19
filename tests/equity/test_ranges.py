"""Tests for opponent range modeling."""

from poker_engine.equity.ranges import OpponentRange


class TestOpponentRangeTight:
    def test_tight_produces_range(self) -> None:
        r = OpponentRange.tight()
        assert r.num_hands > 0

    def test_tight_contains_premium(self) -> None:
        r = OpponentRange.tight()
        assert r.contains("AA")
        assert r.contains("KK")
        assert r.contains("AKs")

    def test_tight_excludes_junk(self) -> None:
        r = OpponentRange.tight()
        assert not r.contains("72o")
        assert not r.contains("32o")

    def test_tight_around_15_percent(self) -> None:
        """Tight range should contain roughly 15% of 169 hands."""
        r = OpponentRange.tight()
        assert 20 <= r.num_hands <= 30


class TestOpponentRangeLoose:
    def test_loose_produces_range(self) -> None:
        r = OpponentRange.loose()
        assert r.num_hands > 0

    def test_loose_contains_more_hands(self) -> None:
        tight = OpponentRange.tight()
        loose = OpponentRange.loose()
        assert loose.num_hands > tight.num_hands

    def test_loose_around_50_percent(self) -> None:
        r = OpponentRange.loose()
        assert 75 <= r.num_hands <= 95

    def test_loose_excludes_worst_junk(self) -> None:
        r = OpponentRange.loose()
        assert not r.contains("72o")


class TestOpponentRangeFromVPIP:
    def test_vpip_zero(self) -> None:
        r = OpponentRange.from_vpip(0.0)
        assert r.num_hands == 0

    def test_vpip_one(self) -> None:
        r = OpponentRange.from_vpip(1.0)
        # Should include all hands
        assert r.num_hands >= 160

    def test_vpip_0_15_similar_to_tight(self) -> None:
        r = OpponentRange.from_vpip(0.15)
        tight = OpponentRange.tight()
        assert abs(r.num_hands - tight.num_hands) <= 2

    def test_vpip_clamped(self) -> None:
        r_neg = OpponentRange.from_vpip(-0.5)
        assert r_neg.num_hands == 0
        r_over = OpponentRange.from_vpip(1.5)
        assert r_over.num_hands >= 160

    def test_vpip_ordering(self) -> None:
        r10 = OpponentRange.from_vpip(0.10)
        r30 = OpponentRange.from_vpip(0.30)
        r50 = OpponentRange.from_vpip(0.50)
        assert r10.num_hands < r30.num_hands < r50.num_hands


class TestOpponentRangeProperties:
    def test_total_weight(self) -> None:
        r = OpponentRange.tight()
        assert r.total_weight == r.num_hands  # all weights are 1.0

    def test_custom_weights(self) -> None:
        r = OpponentRange(hand_weights={"AA": 1.0, "KK": 0.5, "QQ": 0.0})
        assert r.num_hands == 2  # QQ has weight 0
        assert r.contains("AA")
        assert r.contains("KK")
        assert not r.contains("QQ")
        assert r.total_weight == 1.5
