"""Tests for equity cache."""

from poker_engine.core.cards import Card, HandRank, Suit
from poker_engine.core.equity import EquityResult
from poker_engine.equity.cache import EquityCache


def _make_result(win_prob: float = 0.5) -> EquityResult:
    return EquityResult(
        current_hand="Pair of Aces",
        current_rank=HandRank.PAIR,
        win_probability=win_prob,
        tie_probability=0.05,
    )


class TestEquityCache:
    def test_get_miss(self) -> None:
        cache = EquityCache(maxsize=10)
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        assert cache.get(hole, [], 1) is None

    def test_put_and_get(self) -> None:
        cache = EquityCache(maxsize=10)
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        result = _make_result(0.85)
        cache.put(hole, [], 1, result)
        cached = cache.get(hole, [], 1)
        assert cached is not None
        assert cached.win_probability == 0.85

    def test_different_opponents_different_keys(self) -> None:
        cache = EquityCache(maxsize=10)
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        cache.put(hole, [], 1, _make_result(0.85))
        cache.put(hole, [], 2, _make_result(0.73))
        assert cache.get(hole, [], 1).win_probability == 0.85  # type: ignore[union-attr]
        assert cache.get(hole, [], 2).win_probability == 0.73  # type: ignore[union-attr]

    def test_community_cards_in_key(self) -> None:
        cache = EquityCache(maxsize=10)
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        comm1 = [Card(2, Suit.CLUBS), Card(3, Suit.CLUBS), Card(4, Suit.CLUBS)]
        comm2 = [Card(10, Suit.CLUBS), Card(11, Suit.CLUBS), Card(12, Suit.CLUBS)]
        cache.put(hole, comm1, 1, _make_result(0.80))
        cache.put(hole, comm2, 1, _make_result(0.60))
        assert cache.get(hole, comm1, 1).win_probability == 0.80  # type: ignore[union-attr]
        assert cache.get(hole, comm2, 1).win_probability == 0.60  # type: ignore[union-attr]

    def test_lru_eviction(self) -> None:
        cache = EquityCache(maxsize=3)
        cards = [
            [Card(2, Suit.SPADES), Card(3, Suit.SPADES)],
            [Card(4, Suit.SPADES), Card(5, Suit.SPADES)],
            [Card(6, Suit.SPADES), Card(7, Suit.SPADES)],
            [Card(8, Suit.SPADES), Card(9, Suit.SPADES)],
        ]

        cache.put(cards[0], [], 1, _make_result(0.1))
        cache.put(cards[1], [], 1, _make_result(0.2))
        cache.put(cards[2], [], 1, _make_result(0.3))
        assert cache.size == 3

        # Adding a 4th should evict the first (oldest)
        cache.put(cards[3], [], 1, _make_result(0.4))
        assert cache.size == 3
        assert cache.get(cards[0], [], 1) is None  # evicted
        assert cache.get(cards[3], [], 1) is not None

    def test_lru_access_refreshes(self) -> None:
        cache = EquityCache(maxsize=3)
        cards = [
            [Card(2, Suit.SPADES), Card(3, Suit.SPADES)],
            [Card(4, Suit.SPADES), Card(5, Suit.SPADES)],
            [Card(6, Suit.SPADES), Card(7, Suit.SPADES)],
            [Card(8, Suit.SPADES), Card(9, Suit.SPADES)],
        ]

        cache.put(cards[0], [], 1, _make_result(0.1))
        cache.put(cards[1], [], 1, _make_result(0.2))
        cache.put(cards[2], [], 1, _make_result(0.3))

        # Access cards[0] to refresh it
        cache.get(cards[0], [], 1)

        # Now cards[1] is the oldest, should be evicted
        cache.put(cards[3], [], 1, _make_result(0.4))
        assert cache.get(cards[0], [], 1) is not None  # refreshed
        assert cache.get(cards[1], [], 1) is None  # evicted

    def test_size_property(self) -> None:
        cache = EquityCache(maxsize=10)
        assert cache.size == 0
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        cache.put(hole, [], 1, _make_result())
        assert cache.size == 1

    def test_overwrite_existing_key(self) -> None:
        cache = EquityCache(maxsize=10)
        hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]
        cache.put(hole, [], 1, _make_result(0.80))
        cache.put(hole, [], 1, _make_result(0.85))
        assert cache.size == 1
        assert cache.get(hole, [], 1).win_probability == 0.85  # type: ignore[union-attr]

    def test_make_key_is_order_independent(self) -> None:
        """Hole cards in different order should produce the same key."""
        hole_a = [Card(14, Suit.SPADES), Card(13, Suit.HEARTS)]
        hole_b = [Card(13, Suit.HEARTS), Card(14, Suit.SPADES)]
        key_a = EquityCache.make_key(hole_a, [], 1)
        key_b = EquityCache.make_key(hole_b, [], 1)
        assert key_a == key_b
