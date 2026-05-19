"""Console display — inline Rich output (no full-screen TUI)."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from poker_engine.players.random_player import RandomPlayer
from poker_engine.tournament.blind_schedule import BlindSchedule
from poker_engine.tournament.director import TournamentDirector
from poker_engine.tui.console_display import ConsoleDisplay


async def main():
    players = [
        RandomPlayer("Ace", seed=10, fold_weight=0.10, passive_weight=0.75, aggressive_weight=0.15),
        RandomPlayer("Bluff", seed=20, fold_weight=0.15, passive_weight=0.65, aggressive_weight=0.20),
        RandomPlayer("Chips", seed=30, fold_weight=0.10, passive_weight=0.80, aggressive_weight=0.10),
        RandomPlayer("Dealer", seed=40, fold_weight=0.20, passive_weight=0.60, aggressive_weight=0.20),
    ]

    schedule = BlindSchedule.standard()
    director = TournamentDirector(
        players=players,
        blind_schedule=schedule,
        starting_chips=1000,
        seed=42,
        max_hands=15,
    )

    display = ConsoleDisplay(director)
    await display.run()


if __name__ == "__main__":
    asyncio.run(main())
