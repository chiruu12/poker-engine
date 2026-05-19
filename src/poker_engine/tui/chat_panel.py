"""Chat panel showing table talk between players."""

from __future__ import annotations

from collections import deque

from rich.panel import Panel
from rich.text import Text


class ChatPanel:
    """Displays table talk messages from players."""

    def __init__(self, maxlen: int = 12) -> None:
        self._entries: deque[Text] = deque(maxlen=maxlen)

    def add(self, player: str, message: str) -> None:
        truncated = message[:100] + "..." if len(message) > 100 else message
        line = Text()
        line.append(f"{player}: ", style="bold cyan")
        line.append(truncated)
        self._entries.append(line)

    def render(self) -> Panel:
        content = Text()
        for i, entry in enumerate(self._entries):
            if i > 0:
                content.append("\n")
            content.append_text(entry)

        if not self._entries:
            content.append("No table talk yet...", style="dim italic")

        return Panel(
            content,
            title="[bold]Table Talk[/bold]",
            border_style="magenta",
            height=10,
        )
