"""Real model showdown — local LM Studio models play poker.

Uses prompt-based decisions (not tool-calling) since small local
models often don't support function calling reliably.
"""

import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import openai
from rich.console import Console

from poker_engine.core.engine import ActionType, Phase, PokerEngine
from poker_engine.core.equity import calculate_equity
from poker_engine.tui.console_display import ConsoleDisplay
from poker_engine.tournament.blind_schedule import BlindLevel, BlindSchedule
from poker_engine.tournament.director import TournamentDirector

console = Console()

LMSTUDIO_BASE = "http://localhost:1234/v1"


class LocalLLMPlayer:
    """Player powered by a local LM Studio model via prompt-based decisions."""

    def __init__(self, name: str, model_id: str) -> None:
        self._name = name
        self._model_id = model_id
        self._client = openai.AsyncOpenAI(
            base_url=LMSTUDIO_BASE, api_key="not-needed"
        )
        self._last_thought: str | None = None

    @property
    def name(self) -> str:
        return self._name

    async def decide(
        self, game_state: dict[str, Any], valid_actions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        prompt = self._build_prompt(game_state, valid_actions)

        try:
            response = await self._client.chat.completions.create(
                model=self._model_id,
                messages=[
                    {"role": "system", "content": (
                        "You are playing Texas Hold'em poker. "
                        "Analyze the situation and choose the best action. "
                        "Respond with your reasoning on one line, then "
                        "the action number on the last line. Just the number."
                    )},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            raw = response.choices[0].message.content or ""
            self._last_thought = raw.strip()[:120]

            action = self._parse_choice(raw, valid_actions)
            return action

        except Exception as e:
            self._last_thought = f"(error: {e})"
            return self._default_action(valid_actions)

    async def observe(self, event: dict[str, Any]) -> None:
        pass

    async def get_commentary(self) -> str | None:
        return self._last_thought

    def _build_prompt(
        self, game_state: dict[str, Any], valid_actions: list[dict[str, Any]]
    ) -> str:
        lines = [
            f"Phase: {game_state.get('phase', '?')}",
            f"Pot: ${game_state.get('pot', 0)}",
        ]
        cards = game_state.get("hole_cards", [])
        if cards:
            lines.append(f"Your cards: {' '.join(cards)}")
        comm = game_state.get("community_cards", [])
        if comm:
            lines.append(f"Community: {' '.join(comm)}")
        lines.append(f"Your chips: ${game_state.get('your_chips', 0)}")
        lines.append(f"To call: ${game_state.get('current_bet', 0)}")
        lines.append("")
        lines.append("Choose an action:")
        for i, a in enumerate(valid_actions, 1):
            desc = a["action"]
            if a.get("amount"):
                desc += f" (${a['amount']})"
            lines.append(f"  {i}. {desc}")
        lines.append("")
        lines.append("Reply with your choice number.")
        return "\n".join(lines)

    @staticmethod
    def _parse_choice(
        raw: str, valid_actions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        text = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        match = re.search(r"\b(\d+)\b", text.split("\n")[-1])
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < len(valid_actions):
                return valid_actions[idx]

        for line in reversed(text.split("\n")):
            m = re.search(r"\b(\d+)\b", line)
            if m:
                idx = int(m.group(1)) - 1
                if 0 <= idx < len(valid_actions):
                    return valid_actions[idx]

        return LocalLLMPlayer._default_action(valid_actions)

    @staticmethod
    def _default_action(valid_actions: list[dict[str, Any]]) -> dict[str, Any]:
        for a in valid_actions:
            if a["action"] in ("check", "call"):
                return a
        return valid_actions[0] if valid_actions else {"action": "fold"}


async def main():
    models = {
        "LFM-2.5": "liquid/lfm2.5-1.2b",
        "Qwen3": "qwen/qwen3-1.7b",
        "Phi-4": "microsoft/phi-4-mini-reasoning",
    }

    console.print()
    console.rule("[bold cyan]Real Model Poker Showdown[/bold cyan]")
    console.print()
    for name, model_id in models.items():
        console.print(f"  [cyan]{name}[/cyan] → {model_id}")
    console.print()

    players = [LocalLLMPlayer(name, mid) for name, mid in models.items()]

    schedule = BlindSchedule([
        BlindLevel(1, 5, 10, 0, 10),
        BlindLevel(2, 10, 20, 0, 10),
        BlindLevel(3, 25, 50, 5, 10),
    ])

    director = TournamentDirector(
        players=players,
        blind_schedule=schedule,
        starting_chips=500,
        seed=42,
        max_hands=8,
        hand_delay=0.0,
    )

    display = ConsoleDisplay(director, console=console)
    result = await display.run()

    console.print()
    console.rule("[bold]Model Thoughts[/bold]")
    console.print("[dim]Last thought from each model:[/dim]")
    for p in players:
        thought = await p.get_commentary()
        if thought:
            short = thought[:100] + "..." if len(thought) > 100 else thought
            console.print(f"  [cyan]{p.name}[/cyan]: [italic]{short}[/italic]")


if __name__ == "__main__":
    asyncio.run(main())
