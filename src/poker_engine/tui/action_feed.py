"""Scrolling action log for the poker TUI."""

from __future__ import annotations

from collections import deque
from textwrap import shorten

from rich.panel import Panel
from rich.text import Text

from poker_engine.tui.theme import ACTION_COLORS

MAX_LABEL_LEN = 22


class ActionFeed:
    """Scrolling feed of player actions with color-coded entries."""

    def __init__(self, maxlen: int = 20) -> None:
        self._entries: deque[Text] = deque(maxlen=maxlen)

    def add(self, player: str, action: str, amount: int = 0) -> None:
        color = ACTION_COLORS.get(action, "white")
        line = Text()
        line.append(f"{shorten(player, width=MAX_LABEL_LEN, placeholder='...')} ", style="bold")
        if amount > 0:
            line.append(f"{action} ${amount:,}", style=color)
        else:
            line.append(action, style=color)
        self._entries.append(line)

    def add_rich(self, text: Text) -> None:
        self._entries.append(text)

    def render(self, height: int | None = None) -> Panel:
        content = Text()
        max_rows = max(1, (height or 10) - 2)
        entries = list(self._entries)[-max_rows:]

        for i, entry in enumerate(entries):
            if i > 0:
                content.append("\n")
            content.append_text(entry)

        if not self._entries:
            content.append("Waiting for actions...", style="dim")

        return Panel(
            content,
            title="[bold]Actions[/bold]",
            border_style="blue",
            height=height or 10,
        )
