"""Graphic TUI demo — full dashboard with table, actions, thoughts, stats.

Usage: uv run python tmp-playground/run_tui.py
"""

import asyncio
import random
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from poker_engine.players.random_player import RandomPlayer
from poker_engine.tournament.blind_schedule import BlindLevel, BlindSchedule
from poker_engine.tournament.director import TournamentDirector
from poker_engine.tui.app import PokerTUI

THOUGHTS = [
    "Hmm, pot odds look decent here...",
    "This board is scary, might fold.",
    "I've got a strong draw, pushing.",
    "Opponent seems tight, I'll bluff.",
    "Playing it safe this round.",
    "Top pair, gotta bet for value.",
    "Flush draw, need to see another card.",
    "They keep raising, could be a bluff?",
    "Position advantage, let's raise.",
    "Short stack, need to pick a spot.",
    "Two overcards, coin flip territory.",
    "Set mining on a cheap flop.",
]


class ThinkingPlayer:
    """RandomPlayer that generates fake commentary for TUI demo."""

    def __init__(self, name: str, seed: int) -> None:
        self._name = name
        self._inner = RandomPlayer(
            name, seed=seed,
            fold_weight=0.12, passive_weight=0.68, aggressive_weight=0.20,
        )
        self._rng = random.Random(seed + 100)
        self._last_thought: str | None = None

    @property
    def name(self) -> str:
        return self._name

    async def decide(
        self, game_state: dict[str, Any], valid_actions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        self._last_thought = self._rng.choice(THOUGHTS)
        return await self._inner.decide(game_state, valid_actions)

    async def observe(self, event: dict[str, Any]) -> None:
        await self._inner.observe(event)

    async def get_commentary(self) -> str | None:
        return self._last_thought


async def main():
    players = [
        ThinkingPlayer("Alice", seed=10),
        ThinkingPlayer("Bob", seed=20),
        ThinkingPlayer("Charlie", seed=30),
        ThinkingPlayer("Diana", seed=40),
    ]

    schedule = BlindSchedule([
        BlindLevel(1, 5, 10, 0, 15),
        BlindLevel(2, 10, 20, 0, 15),
        BlindLevel(3, 25, 50, 5, 15),
    ])

    director = TournamentDirector(
        players=players,
        blind_schedule=schedule,
        starting_chips=2000,
        seed=42,
        max_hands=15,
        hand_delay=1.5,
    )

    tui = PokerTUI(director)
    result = await tui.run()

    print(f"\nTournament done! {result.hands_played} hands.")
    for i, s in enumerate(result.standings, 1):
        print(f"  #{i} {s['name']}: ${s['chips']:,}")


if __name__ == "__main__":
    asyncio.run(main())
