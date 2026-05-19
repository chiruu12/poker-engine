"""Tight table — bots that mostly check/call, so we see full hand progressions."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table as RichTable

from poker_engine.players.random_player import RandomPlayer
from poker_engine.tournament.blind_schedule import BlindLevel, BlindSchedule
from poker_engine.tournament.director import TournamentDirector
from poker_engine.tournament.events import (
    ActionEvent,
    BlindLevelEvent,
    EliminationEvent,
    HandEndEvent,
    HandStartEvent,
    PhaseChangeEvent,
)

console = Console()
SUIT_COLORS = {"♥": "red", "♦": "red", "♠": "white", "♣": "white"}
ACTION_COLORS = {
    "fold": "red", "call": "green", "check": "dim green",
    "raise": "yellow", "all_in": "bold magenta",
}


def cc(cards):
    parts = []
    for c in cards:
        for s, col in SUIT_COLORS.items():
            if s in c:
                parts.append(f"[{col}]{c}[/{col}]")
                break
        else:
            parts.append(c)
    return " ".join(parts)


hand_count = [0]


def handle(event):
    if isinstance(event, HandStartEvent):
        hand_count[0] = event.hand_num
        console.print()
        console.rule(f"[bold cyan]Hand #{event.hand_num}[/bold cyan]  Dealer: {event.dealer}")

    elif isinstance(event, PhaseChangeEvent):
        console.print(f"\n  [bold yellow]{event.phase:>5}[/bold yellow]  {cc(event.community)}")

    elif isinstance(event, ActionEvent):
        col = ACTION_COLORS.get(event.action, "white")
        amt = f" ${event.amount}" if event.action == "raise" and event.amount else ""
        if event.action == "all_in":
            amt = " ALL-IN"
        console.print(f"    [{col}]{event.player:>8}: {event.action}{amt}[/{col}]  [dim]pot ${event.pot}[/dim]")

    elif isinstance(event, HandEndEvent):
        console.print(f"\n  [bold green]>>> {', '.join(event.winners)} wins ({event.win_reason})[/bold green]")

    elif isinstance(event, EliminationEvent):
        console.print(f"  [bold red]>>> {event.player} eliminated #{event.position}[/bold red]")


async def main():
    # Tight bots: 5% fold, 90% check/call, 5% raise
    names = ["Nit", "Rock", "Mouse", "Passive"]
    players = [
        RandomPlayer(n, seed=i * 13, fold_weight=0.05, passive_weight=0.90, aggressive_weight=0.05)
        for i, n in enumerate(names)
    ]

    # Slow blinds so we see lots of hands
    schedule = BlindSchedule([
        BlindLevel(1, 5, 10, 0, 20),
        BlindLevel(2, 10, 20, 0, 20),
        BlindLevel(3, 25, 50, 5, 20),
    ])

    console.print(Panel.fit(
        "[bold cyan]Tight Table Demo[/bold cyan]\n"
        "4 passive bots (90% check/call) — full hand progressions\n"
        "Starting: $2,000 each | Blinds: 5/10",
        border_style="green",
    ))

    director = TournamentDirector(
        players=players,
        blind_schedule=schedule,
        starting_chips=2000,
        seed=99,
        max_hands=12,
    )
    director.on_event(handle)

    result = await director.run()

    # Standings
    console.print()
    console.rule("[bold]Standings after 12 hands[/bold]")
    table = RichTable(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=3)
    table.add_column("Player", style="cyan", width=10)
    table.add_column("Chips", justify="right", style="green")
    table.add_column("Won", justify="right")
    table.add_column("Played", justify="right")

    max_c = max((s["chips"] for s in result.standings), default=1) or 1
    for i, s in enumerate(result.standings, 1):
        bar = "█" * int(15 * s["chips"] / max_c) + "░" * (15 - int(15 * s["chips"] / max_c))
        table.add_row(str(i), s["name"], f"${s['chips']:,}", str(s["hands_won"]), str(s["hands_played"]))

    console.print(table)
    console.print(f"\n[dim]{result.hands_played} hands played[/dim]")


if __name__ == "__main__":
    asyncio.run(main())
