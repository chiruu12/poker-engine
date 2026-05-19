"""Card rendering with Unicode suits and Rich markup.

SUIT_STYLES is the single source of truth for card coloring.
Import it from here rather than redefining in other modules.
"""

from __future__ import annotations

SUIT_STYLES: dict[str, str] = {
    "♥": "bold red",
    "♦": "bold red",
    "♠": "bold blue",
    "♣": "bold blue",
}


def style_for_card(card_str: str) -> str:
    """Return the Rich style for a card string based on its suit."""
    suit_char = card_str[-1] if card_str else ""
    return SUIT_STYLES.get(suit_char, "white")


def render_card(card_str: str, face_down: bool = False) -> str:
    """Render a single card with Rich markup."""
    if face_down:
        return "[dim]??[/dim]"
    style = style_for_card(card_str)
    return f"[{style}]{card_str}[/{style}]"


def render_hand(cards: list[str]) -> str:
    """Render multiple cards separated by spaces."""
    return " ".join(render_card(c) for c in cards)
