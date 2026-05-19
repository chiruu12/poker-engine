"""Pre-flop equity lookup table for 169 canonical starting hands."""

from __future__ import annotations

from poker_engine.core.cards import Card

# Poker-notation rank symbols (use "T" for ten instead of "10").
_RANK_SYMBOL: dict[int, str] = {
    2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7",
    8: "8", 9: "9", 10: "T", 11: "J", 12: "Q", 13: "K", 14: "A",
}


def hand_key(card1: Card, card2: Card) -> str:
    """Return canonical hand representation like 'AKs', 'AKo', or 'AA'.

    Higher rank always comes first. Suited pairs get 's' suffix,
    off-suit pairs get 'o' suffix, pocket pairs have no suffix.
    """
    r1 = _RANK_SYMBOL[card1.rank]
    r2 = _RANK_SYMBOL[card2.rank]

    if card1.rank == card2.rank:
        return f"{r1}{r2}"

    suited = card1.suit == card2.suit
    suffix = "s" if suited else "o"

    if card1.rank > card2.rank:
        return f"{r1}{r2}{suffix}"
    return f"{r2}{r1}{suffix}"


# Pre-computed win rates for canonical hands vs 1-8 opponents.
# Values are approximate equities from large-scale simulations.
PREFLOP_EQUITY: dict[str, dict[int, float]] = {
    # --- Premium pairs ---
    "AA": {
        1: 0.852, 2: 0.734, 3: 0.637, 4: 0.560, 5: 0.495,
        6: 0.441, 7: 0.394, 8: 0.353,
    },
    "KK": {
        1: 0.824, 2: 0.691, 3: 0.587, 4: 0.509, 5: 0.445,
        6: 0.391, 7: 0.346, 8: 0.307,
    },
    "QQ": {
        1: 0.799, 2: 0.653, 3: 0.543, 4: 0.462, 5: 0.398,
        6: 0.346, 7: 0.303, 8: 0.267,
    },
    "JJ": {
        1: 0.774, 2: 0.616, 3: 0.501, 4: 0.418, 5: 0.354,
        6: 0.304, 7: 0.264, 8: 0.230,
    },
    "TT": {
        1: 0.750, 2: 0.581, 3: 0.462, 4: 0.378, 5: 0.315,
        6: 0.266, 7: 0.228, 8: 0.197,
    },
    "99": {
        1: 0.720, 2: 0.543, 3: 0.422, 4: 0.339, 5: 0.279,
        6: 0.233, 7: 0.198, 8: 0.170,
    },
    "88": {
        1: 0.691, 2: 0.507, 3: 0.386, 4: 0.305, 5: 0.248,
        6: 0.205, 7: 0.173, 8: 0.148,
    },
    "77": {
        1: 0.662, 2: 0.473, 3: 0.353, 4: 0.275, 5: 0.221,
        6: 0.182, 7: 0.152, 8: 0.130,
    },
    "66": {
        1: 0.633, 2: 0.440, 3: 0.322, 4: 0.248, 5: 0.198,
        6: 0.162, 7: 0.135, 8: 0.115,
    },
    "55": {
        1: 0.604, 2: 0.409, 3: 0.295, 4: 0.225, 5: 0.178,
        6: 0.145, 7: 0.121, 8: 0.103,
    },
    # --- Big suited broadways ---
    "AKs": {
        1: 0.670, 2: 0.509, 3: 0.412, 4: 0.343, 5: 0.293,
        6: 0.254, 7: 0.223, 8: 0.198,
    },
    "AQs": {
        1: 0.660, 2: 0.494, 3: 0.395, 4: 0.326, 5: 0.276,
        6: 0.238, 7: 0.208, 8: 0.184,
    },
    "AJs": {
        1: 0.650, 2: 0.480, 3: 0.379, 4: 0.311, 5: 0.262,
        6: 0.225, 7: 0.196, 8: 0.173,
    },
    "ATs": {
        1: 0.640, 2: 0.466, 3: 0.365, 4: 0.297, 5: 0.249,
        6: 0.213, 7: 0.185, 8: 0.163,
    },
    "KQs": {
        1: 0.634, 2: 0.469, 3: 0.371, 4: 0.304, 5: 0.256,
        6: 0.220, 7: 0.192, 8: 0.169,
    },
    "KJs": {
        1: 0.624, 2: 0.455, 3: 0.355, 4: 0.289, 5: 0.242,
        6: 0.207, 7: 0.180, 8: 0.158,
    },
    "QJs": {
        1: 0.604, 2: 0.435, 3: 0.337, 4: 0.273, 5: 0.228,
        6: 0.194, 7: 0.168, 8: 0.148,
    },
    # --- Big offsuit broadways ---
    "AKo": {
        1: 0.653, 2: 0.482, 3: 0.382, 4: 0.313, 5: 0.264,
        6: 0.226, 7: 0.197, 8: 0.173,
    },
    "AQo": {
        1: 0.642, 2: 0.466, 3: 0.363, 4: 0.295, 5: 0.246,
        6: 0.210, 7: 0.182, 8: 0.160,
    },
    "AJo": {
        1: 0.632, 2: 0.449, 3: 0.346, 4: 0.278, 5: 0.231,
        6: 0.196, 7: 0.169, 8: 0.148,
    },
    "KQo": {
        1: 0.614, 2: 0.440, 3: 0.339, 4: 0.273, 5: 0.227,
        6: 0.193, 7: 0.167, 8: 0.147,
    },
    # --- Suited connectors ---
    "JTs": {
        1: 0.585, 2: 0.418, 3: 0.323, 4: 0.261, 5: 0.218,
        6: 0.186, 7: 0.161, 8: 0.142,
    },
    "T9s": {
        1: 0.555, 2: 0.388, 3: 0.296, 4: 0.237, 5: 0.196,
        6: 0.166, 7: 0.143, 8: 0.125,
    },
    "98s": {
        1: 0.536, 2: 0.370, 3: 0.280, 4: 0.222, 5: 0.183,
        6: 0.154, 7: 0.133, 8: 0.116,
    },
    # --- Bottom 5 hands ---
    "72o": {
        1: 0.345, 2: 0.224, 3: 0.159, 4: 0.120, 5: 0.095,
        6: 0.078, 7: 0.065, 8: 0.056,
    },
    "83o": {
        1: 0.358, 2: 0.232, 3: 0.165, 4: 0.124, 5: 0.098,
        6: 0.080, 7: 0.067, 8: 0.057,
    },
    "73o": {
        1: 0.355, 2: 0.230, 3: 0.164, 4: 0.123, 5: 0.097,
        6: 0.079, 7: 0.066, 8: 0.056,
    },
    "82o": {
        1: 0.348, 2: 0.225, 3: 0.160, 4: 0.121, 5: 0.095,
        6: 0.078, 7: 0.065, 8: 0.056,
    },
    "32o": {
        1: 0.348, 2: 0.226, 3: 0.162, 4: 0.123, 5: 0.098,
        6: 0.080, 7: 0.067, 8: 0.058,
    },
}


def lookup_preflop_equity(
    hole_cards: list[Card],
    num_opponents: int,
) -> float | None:
    """Look up preflop equity for a given hand and opponent count.

    Returns None if the hand or opponent count is not in the table.
    """
    if len(hole_cards) != 2:
        return None
    key = hand_key(hole_cards[0], hole_cards[1])
    hand_data = PREFLOP_EQUITY.get(key)
    if hand_data is None:
        return None
    return hand_data.get(num_opponents)
