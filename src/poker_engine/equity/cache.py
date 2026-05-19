"""Simple LRU cache for equity calculations."""

from __future__ import annotations

from collections import OrderedDict

from poker_engine.core.cards import Card
from poker_engine.core.equity import EquityResult


class EquityCache:
    """LRU cache for equity computation results.

    Keys are derived from (hole_cards, community_cards, num_opponents).
    """

    # Type alias for cache keys
    _CacheKey = tuple[frozenset[tuple[int, int]], frozenset[tuple[int, int]], int]

    def __init__(self, maxsize: int = 1024) -> None:
        self._maxsize = maxsize
        self._cache: OrderedDict[EquityCache._CacheKey, EquityResult] = OrderedDict()

    @staticmethod
    def make_key(
        hole_cards: list[Card],
        community_cards: list[Card],
        num_opponents: int,
    ) -> tuple[frozenset[tuple[int, int]], frozenset[tuple[int, int]], int]:
        """Create a hashable cache key from cards and opponent count."""
        hole = frozenset((c.rank, c.suit) for c in hole_cards)
        community = frozenset((c.rank, c.suit) for c in community_cards)
        return (hole, community, num_opponents)

    def get(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        num_opponents: int,
    ) -> EquityResult | None:
        """Retrieve a cached result, or None if not found."""
        key = self.make_key(hole_cards, community_cards, num_opponents)
        if key in self._cache:
            self._cache.move_to_end(key)
            return self._cache[key]
        return None

    def put(
        self,
        hole_cards: list[Card],
        community_cards: list[Card],
        num_opponents: int,
        result: EquityResult,
    ) -> None:
        """Store a result in the cache, evicting the oldest entry if full."""
        key = self.make_key(hole_cards, community_cards, num_opponents)
        if key in self._cache:
            self._cache.move_to_end(key)
            self._cache[key] = result
        else:
            if len(self._cache) >= self._maxsize:
                self._cache.popitem(last=False)
            self._cache[key] = result

    @property
    def size(self) -> int:
        """Current number of entries in the cache."""
        return len(self._cache)
