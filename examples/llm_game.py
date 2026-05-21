#!/usr/bin/env python3
"""LLM game -- 3 local models via LM Studio, console display."""

import asyncio
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import openai

from poker_engine.tournament.blind_schedule import BlindLevel, BlindSchedule
from poker_engine.tournament.director import TournamentDirector
from poker_engine.tui.console_display import ConsoleDisplay


class LocalPlayer:
    """Prompt-based LLM player for local models via LM Studio."""

    def __init__(self, name: str, model_id: str, personality: str = "") -> None:
        self._name = name
        self._model_id = model_id
        self._personality = personality
        self._client = openai.AsyncOpenAI(
            base_url="http://localhost:1234/v1", api_key="not-needed"
        )
        self._last_thought: str | None = None

    @property
    def name(self) -> str:
        return self._name

    async def decide(
        self, game_state: dict[str, Any], valid_actions: list[dict[str, Any]]
    ) -> dict[str, Any]:
        system = (
            "You are playing Texas Hold'em poker. "
            "Analyze and choose the best action. "
            "Respond with reasoning, then the action number on the last line."
        )
        if self._personality:
            system += f"\n\n{self._personality}"

        prompt = self._build_prompt(game_state, valid_actions)
        try:
            resp = await self._client.chat.completions.create(
                model=self._model_id,
                messages=[
                    {"role": "system", "content": system},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                temperature=0.7,
            )
            raw = resp.choices[0].message.content or ""
            self._last_thought = raw.strip()[:120]
            return self._parse(raw, valid_actions)
        except Exception:
            self._last_thought = None
            return _default(valid_actions)

    async def observe(self, event: dict[str, Any]) -> None:
        pass

    async def get_commentary(self) -> str | None:
        return self._last_thought

    async def get_table_talk(self, game_state: dict[str, Any]) -> str | None:
        return None

    def _build_prompt(
        self, gs: dict[str, Any], actions: list[dict[str, Any]]
    ) -> str:
        lines = [f"Phase: {gs.get('phase', '?')}", f"Pot: ${gs.get('pot', 0)}"]
        if gs.get("hole_cards"):
            lines.append(f"Your cards: {' '.join(gs['hole_cards'])}")
        if gs.get("community_cards"):
            lines.append(f"Community: {' '.join(gs['community_cards'])}")
        lines.append(f"Your chips: ${gs.get('your_chips', 0)}")
        lines.append(f"To call: ${gs.get('current_bet', 0)}")
        lines.append("\nChoose an action:")
        for i, a in enumerate(actions, 1):
            d = a["action"] + (f" (${a['amount']})" if a.get("amount") else "")
            lines.append(f"  {i}. {d}")
        lines.append("\nReply with your choice number.")
        return "\n".join(lines)

    @staticmethod
    def _parse(raw: str, actions: list[dict[str, Any]]) -> dict[str, Any]:
        text = re.sub(r"<think>.*?</think>", "", raw, flags=re.DOTALL).strip()
        for line in reversed(text.split("\n")):
            m = re.search(r"\b(\d+)\b", line)
            if m:
                idx = int(m.group(1)) - 1
                if 0 <= idx < len(actions):
                    return actions[idx]
        return _default(actions)


def _default(actions: list[dict[str, Any]]) -> dict[str, Any]:
    for a in actions:
        if a["action"] in ("check", "call"):
            return a
    return actions[0] if actions else {"action": "fold"}


async def main() -> None:
    players = [
        LocalPlayer("LFM-2.5", "liquid/lfm2.5-1.2b"),
        LocalPlayer("Qwen3", "qwen/qwen3-1.7b"),
        LocalPlayer("Phi-4", "microsoft/phi-4-mini-reasoning"),
    ]

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
        max_hands=10,
    )

    display = ConsoleDisplay(director)
    await display.run()


if __name__ == "__main__":
    asyncio.run(main())
