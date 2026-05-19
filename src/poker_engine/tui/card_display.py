"""Card rendering with Unicode suits and Rich markup."""

from __future__ import annotations

SUIT_STYLES = {"♥": "bold red", "♦": "bold red", "♠": "bold blue", "♣": "bold blue"}


def render_card(card_str: str, face_down: bool = False) -> str:
    """Render a single card string with Rich markup.

    Hearts/diamonds in red, clubs/spades in blue.
    """
    if face_down:
        return "[dim]??[/dim]"

    suit_char = card_str[-1] if card_str else ""
    style = SUIT_STYLES.get(suit_char, "white")
    return f"[{style}]{card_str}[/{style}]"


def render_hand(cards: list[str]) -> str:
    """Render multiple cards separated by spaces."""
    return " ".join(render_card(c) for c in cards)
