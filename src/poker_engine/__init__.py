"""Poker Engine — Pure Texas Hold'em for AI agents."""

__version__ = "0.1.0"

from poker_engine.cards import (
    Card,
    HandRank,
    HandResult,
    Suit,
    describe_hand,
    evaluate_hand,
    make_deck,
)
from poker_engine.engine import (
    Action,
    ActionResult,
    ActionType,
    HandSummary,
    Phase,
    PlayerState,
    PokerEngine,
    ShowdownResult,
    SidePot,
)
from poker_engine.equity import EquityResult, calculate_equity

__all__ = [
    "Action",
    "ActionResult",
    "ActionType",
    "Card",
    "EquityResult",
    "HandRank",
    "HandResult",
    "HandSummary",
    "Phase",
    "PlayerState",
    "PokerEngine",
    "ShowdownResult",
    "SidePot",
    "Suit",
    "calculate_equity",
    "describe_hand",
    "evaluate_hand",
    "make_deck",
]
