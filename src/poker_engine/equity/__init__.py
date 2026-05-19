"""Enhanced equity calculation — preflop tables, caching, and range modeling."""

# Re-export core equity symbols so that ``from poker_engine.equity import
# calculate_equity`` (used by existing tests via the old sys.modules alias)
# keeps working now that poker_engine.equity is a real package.
from poker_engine.core.equity import EquityResult, calculate_equity
from poker_engine.equity.cache import EquityCache
from poker_engine.equity.monte_carlo import calculate_equity_v2
from poker_engine.equity.preflop import (
    PREFLOP_EQUITY,
    hand_key,
    lookup_preflop_equity,
)
from poker_engine.equity.ranges import OpponentRange

__all__ = [
    "EquityResult",
    "PREFLOP_EQUITY",
    "EquityCache",
    "OpponentRange",
    "calculate_equity",
    "calculate_equity_v2",
    "hand_key",
    "lookup_preflop_equity",
]
