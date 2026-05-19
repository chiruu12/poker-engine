"""Enhanced Monte Carlo equity calculator with preflop lookup and caching."""

from __future__ import annotations

from poker_engine.core.cards import Card
from poker_engine.core.equity import EquityResult, calculate_equity
from poker_engine.equity.cache import EquityCache
from poker_engine.equity.preflop import lookup_preflop_equity

# Module-level shared cache instance
_default_cache = EquityCache(maxsize=1024)


def calculate_equity_v2(
    hole_cards: list[Card],
    community_cards: list[Card],
    num_opponents: int,
    num_simulations: int = 2000,
    seed: int | None = None,
    use_preflop_table: bool = True,
    cache: EquityCache | None = None,
) -> EquityResult:
    """Calculate equity with preflop lookup table and caching.

    Tries preflop lookup first when no community cards are dealt.
    Uses cache to avoid redundant Monte Carlo runs.
    Falls back to core Monte Carlo simulation otherwise.

    Args:
        hole_cards: Player's two hole cards.
        community_cards: Community cards dealt so far (0-5).
        num_opponents: Number of opponents.
        num_simulations: Monte Carlo iterations (default 2000).
        seed: Random seed for reproducibility.
        use_preflop_table: Whether to try the preflop lookup table.
        cache: Optional cache instance. Uses module default if None.

    Returns:
        EquityResult with win/tie probabilities.
    """
    equity_cache = cache if cache is not None else _default_cache

    # Check cache first
    cached = equity_cache.get(hole_cards, community_cards, num_opponents)
    if cached is not None:
        return cached

    # Try preflop lookup when no community cards
    if use_preflop_table and len(community_cards) == 0:
        preflop_equity = lookup_preflop_equity(hole_cards, num_opponents)
        if preflop_equity is not None:
            from poker_engine.core.cards import HandRank

            result = EquityResult(
                current_hand="Pre-flop",
                current_rank=HandRank.HIGH_CARD,
                win_probability=preflop_equity,
                tie_probability=0.0,
            )
            equity_cache.put(hole_cards, community_cards, num_opponents, result)
            return result

    # Fall back to Monte Carlo simulation
    result = calculate_equity(
        hole_cards=hole_cards,
        community_cards=community_cards,
        num_opponents=num_opponents,
        num_simulations=num_simulations,
        seed=seed,
    )

    equity_cache.put(hole_cards, community_cards, num_opponents, result)
    return result
