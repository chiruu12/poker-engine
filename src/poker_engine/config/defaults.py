"""Built-in default configurations as plain dicts."""

from __future__ import annotations

DEFAULT_TOURNAMENT: dict = {
    "name": "Default Tournament",
    "max_players": 9,
    "starting_chips": 1000,
    "blind_structure": "standard",
    "payout_structure": "top_3",
    "hand_delay": 1.0,
    "seed": None,
}

DEFAULT_AGENT: dict = {
    "name": "Bot",
    "type": "random",
    "model": "",
    "provider": "anthropic",
    "api_key_env": "",
    "personality": "",
    "temperature": 0.7,
    "system_prompt": "",
}

STANDARD_BLINDS: dict = {
    "levels": [
        {"level": 1, "small_blind": 10, "big_blind": 20, "ante": 0, "duration_hands": 10},
        {"level": 2, "small_blind": 15, "big_blind": 30, "ante": 0, "duration_hands": 10},
        {"level": 3, "small_blind": 25, "big_blind": 50, "ante": 5, "duration_hands": 10},
        {"level": 4, "small_blind": 50, "big_blind": 100, "ante": 10, "duration_hands": 10},
        {"level": 5, "small_blind": 75, "big_blind": 150, "ante": 15, "duration_hands": 10},
        {"level": 6, "small_blind": 100, "big_blind": 200, "ante": 25, "duration_hands": 10},
        {"level": 7, "small_blind": 150, "big_blind": 300, "ante": 50, "duration_hands": 10},
        {"level": 8, "small_blind": 250, "big_blind": 500, "ante": 50, "duration_hands": 10},
    ],
}

TURBO_BLINDS: dict = {
    "levels": [
        {"level": 1, "small_blind": 10, "big_blind": 20, "ante": 0, "duration_hands": 5},
        {"level": 2, "small_blind": 15, "big_blind": 30, "ante": 0, "duration_hands": 5},
        {"level": 3, "small_blind": 25, "big_blind": 50, "ante": 5, "duration_hands": 5},
        {"level": 4, "small_blind": 50, "big_blind": 100, "ante": 10, "duration_hands": 5},
        {"level": 5, "small_blind": 75, "big_blind": 150, "ante": 15, "duration_hands": 5},
        {"level": 6, "small_blind": 100, "big_blind": 200, "ante": 25, "duration_hands": 5},
        {"level": 7, "small_blind": 150, "big_blind": 300, "ante": 50, "duration_hands": 5},
        {"level": 8, "small_blind": 250, "big_blind": 500, "ante": 50, "duration_hands": 5},
    ],
}
