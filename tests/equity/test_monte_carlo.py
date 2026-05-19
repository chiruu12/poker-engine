"""Tests for enhanced Monte Carlo equity calculator (v2)."""

from poker_engine.core.cards import Card, Suit
from poker_engine.core.equity import calculate_equity
from poker_engine.equity.cache import EquityCache
from poker_engine.equity.monte_carlo import calculate_equity_v2


class TestCalculateEquityV2:
    def test_preflop_lookup_used_for_known_hand(self) -> None:
        """AA vs 1 should use the preflop table and return known equity."""
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        result = calculate_equity_v2(hole, [], 1, cache=EquityCache())
        assert result.win_probability == 0.852
        assert result.current_hand == "Pre-flop"

    def test_preflop_lookup_used_for_72o(self) -> None:
        hole = [Card(7, Suit.DIAMONDS), Card(2, Suit.CLUBS)]
        result = calculate_equity_v2(hole, [], 1, cache=EquityCache())
        assert result.win_probability == 0.345

    def test_preflop_lookup_disabled(self) -> None:
        """When use_preflop_table=False, should use Monte Carlo."""
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        result = calculate_equity_v2(
            hole,
            [],
            1,
            seed=42,
            use_preflop_table=False,
            cache=EquityCache(),
        )
        # Should still be a high equity, but from Monte Carlo, not exact table value
        assert result.win_probability > 0.7
        assert result.current_hand != "Pre-flop"

    def test_with_community_cards_uses_monte_carlo(self) -> None:
        """When community cards exist, preflop table doesn't apply."""
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        community = [Card(2, Suit.CLUBS), Card(7, Suit.DIAMONDS), Card(10, Suit.HEARTS)]
        result = calculate_equity_v2(
            hole,
            community,
            1,
            seed=42,
            cache=EquityCache(),
        )
        # AA on a low board should still have high equity
        assert result.win_probability > 0.5

    def test_cache_is_populated(self) -> None:
        """After calculation, the result should be in cache."""
        cache = EquityCache()
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        calculate_equity_v2(hole, [], 1, cache=cache)
        assert cache.size == 1
        # Second call should hit cache
        result2 = calculate_equity_v2(hole, [], 1, cache=cache)
        assert result2.win_probability == 0.852

    def test_cache_hit_returns_same_result(self) -> None:
        """Cached results should be returned on repeated calls."""
        cache = EquityCache()
        hole = [Card(13, Suit.SPADES), Card(13, Suit.HEARTS)]
        r1 = calculate_equity_v2(hole, [], 1, cache=cache)
        r2 = calculate_equity_v2(hole, [], 1, cache=cache)
        assert r1.win_probability == r2.win_probability

    def test_v2_similar_to_core_for_postflop(self) -> None:
        """V2 Monte Carlo should give similar results to core for postflop."""
        hole = [Card(14, Suit.SPADES), Card(13, Suit.SPADES)]
        community = [
            Card(12, Suit.SPADES),
            Card(11, Suit.SPADES),
            Card(2, Suit.HEARTS),
        ]
        core_result = calculate_equity(hole, community, 1, num_simulations=2000, seed=42)
        v2_result = calculate_equity_v2(
            hole,
            community,
            1,
            num_simulations=2000,
            seed=42,
            cache=EquityCache(),
        )
        # Should be close (same seed, same underlying calculation)
        assert abs(core_result.win_probability - v2_result.win_probability) < 0.01

    def test_zero_opponents(self) -> None:
        """With zero opponents, should always win."""
        hole = [Card(7, Suit.DIAMONDS), Card(2, Suit.CLUBS)]
        result = calculate_equity_v2(hole, [], 0, cache=EquityCache())
        assert result.win_probability == 1.0

    def test_cache_hit_skips_lookup(self) -> None:
        """Regression: second call must read from cache, not re-run lookup."""
        from unittest.mock import patch

        cache = EquityCache()
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        calculate_equity_v2(hole, [], 1, cache=cache)
        assert cache.size == 1

        with patch("poker_engine.equity.monte_carlo.lookup_preflop_equity") as mock_lookup:
            result = calculate_equity_v2(hole, [], 1, cache=cache)
            mock_lookup.assert_not_called()
        assert result.win_probability == 0.852

    def test_unknown_preflop_hand_falls_back_to_monte_carlo(self) -> None:
        """A hand not in the preflop table should still work via Monte Carlo."""
        # 94o is not in the table
        hole = [Card(9, Suit.SPADES), Card(4, Suit.HEARTS)]
        result = calculate_equity_v2(
            hole,
            [],
            1,
            seed=42,
            cache=EquityCache(),
        )
        assert 0.0 < result.win_probability < 1.0
        assert result.current_rank is not None
