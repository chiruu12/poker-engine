#!/usr/bin/env python3
"""Quick game -- 3 random bots, minimal display."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from poker_engine.players.random_player import RandomPlayer
from poker_engine.tournament.blind_schedule import BlindLevel, BlindSchedule
from poker_engine.tournament.director import TournamentDirector
from poker_engine.tui.minimal_display import MinimalDisplay


async def main() -> None:
    players = [
        RandomPlayer("Alice", seed=1),
        RandomPlayer("Bob", seed=2),
        RandomPlayer("Charlie", seed=3),
    ]

    schedule = BlindSchedule([
        BlindLevel(1, 10, 20, 0, 10),
        BlindLevel(2, 25, 50, 5, 10),
    ])

    director = TournamentDirector(
        players=players,
        blind_schedule=schedule,
        starting_chips=500,
        seed=42,
        max_hands=10,
    )

    display = MinimalDisplay(director)
    await display.run()


if __name__ == "__main__":
    asyncio.run(main())
