"""Longer tournament — 6 players, deeper stacks, more hands to watch."""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table as RichTable

from poker_engine.players.random_player import RandomPlayer
from poker_engine.tournament.blind_schedule import BlindSchedule
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
    "fold": "red",
    "call": "green",
    "check": "dim green",
    "raise": "yellow",
    "all_in": "bold magenta",
}


def colorize_cards(cards: list[str]) -> str:
    parts = []
    for c in cards:
        colored = c
        for suit, color in SUIT_COLORS.items():
            if suit in c:
                colored = f"[{color}]{c}[/{color}]"
                break
        parts.append(colored)
    return " ".join(parts)


current_blind = {"sb": 10, "bb": 20}


def handle_event(event):
    if isinstance(event, HandStartEvent):
        console.print()
        console.rule(
            f"[bold cyan]Hand #{event.hand_num}[/bold cyan]  "
            f"Dealer: {event.dealer}  "
            f"Blinds: {current_blind['sb']}/{current_blind['bb']}"
        )

    elif isinstance(event, PhaseChangeEvent):
        cards = colorize_cards(event.community)
        console.print(f"\n  [bold yellow]{event.phase:>5}[/bold yellow]  {cards}")

    elif isinstance(event, ActionEvent):
        color = ACTION_COLORS.get(event.action, "white")
        amt = ""
        if event.action == "raise" and event.amount:
            amt = f" to ${event.amount}"
        elif event.action == "all_in":
            amt = " ALL IN"
        console.print(
            f"    [{color}]{event.player:>10}: {event.action}{amt}[/{color}]"
            f"  [dim]pot ${event.pot}[/dim]"
        )

    elif isinstance(event, HandEndEvent):
        console.print(
            f"\n  [bold green]>>> {', '.join(event.winners)} wins[/bold green]"
            f" ({event.win_reason})"
        )

    elif isinstance(event, BlindLevelEvent):
        current_blind["sb"] = event.small_blind
        current_blind["bb"] = event.big_blind

    elif isinstance(event, EliminationEvent):
        console.print(
            f"  [bold red]>>> {event.player} busted out (#{event.position})[/bold red]"
        )


async def main():
    names = ["Ace", "Bluff", "Chips", "Dealer", "Edge", "Fish"]
    console.print(Panel.fit(
        f"[bold cyan]6-Player Sit & Go[/bold cyan]\n"
        f"Players: {', '.join(names)}\n"
        f"Starting chips: 1,500 | Blinds: standard schedule",
        border_style="green",
    ))

    players = [RandomPlayer(n, seed=i * 7 + 3) for i, n in enumerate(names)]

    schedule = BlindSchedule.standard()
    director = TournamentDirector(
        players=players,
        blind_schedule=schedule,
        starting_chips=1500,
        seed=77,
        max_hands=30,
    )

    director.on_event(handle_event)
    result = await director.run()

    console.print()
    console.rule("[bold]Final Standings[/bold]")

    table = RichTable(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=3)
    table.add_column("Player", style="cyan", width=10)
    table.add_column("Chips", justify="right", style="green")
    table.add_column("Won", justify="right")
    table.add_column("Played", justify="right")
    table.add_column("Bar", width=25)

    max_chips = max((s["chips"] for s in result.standings), default=1) or 1
    for i, s in enumerate(result.standings, 1):
        bar_len = int(20 * s["chips"] / max_chips) if max_chips else 0
        bar = "█" * bar_len + "░" * (20 - bar_len)
        table.add_row(
            str(i),
            s["name"],
            f"${s['chips']:,}",
            str(s["hands_won"]),
            str(s["hands_played"]),
            f"[green]{bar}[/green]",
        )

    console.print(table)
    console.print(f"\n[dim]{result.hands_played} hands played[/dim]")

    if result.payouts:
        console.print("\n[bold]Payouts:[/bold]")
        for p in result.payouts:
            console.print(f"  #{p['place']}: {p['player']} — ${p['amount']:,}")


if __name__ == "__main__":
    asyncio.run(main())
