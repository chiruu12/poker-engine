"""Opponent range modeling for equity analysis."""

from __future__ import annotations

from dataclasses import dataclass, field

# Canonical hand rankings from strongest to weakest (169 total).
# This is a simplified ordering used for range construction.
_HAND_TIERS: list[str] = [
    # Tier 1: Premium (top ~3%)
    "AA",
    "KK",
    "QQ",
    "AKs",
    "JJ",
    # Tier 2: Strong (top ~6%)
    "AQs",
    "KQs",
    "AKo",
    "TT",
    # Tier 3: Good (top ~10%)
    "AJs",
    "KJs",
    "AQo",
    "99",
    "ATs",
    "QJs",
    # Tier 4: Playable (top ~15%)
    "KQo",
    "KTs",
    "88",
    "QTs",
    "AJo",
    "JTs",
    "A9s",
    "77",
    # Tier 5: Marginal (top ~25%)
    "KJo",
    "A8s",
    "T9s",
    "QJo",
    "K9s",
    "A7s",
    "66",
    "A5s",
    "A6s",
    "A4s",
    "55",
    "J9s",
    "KTo",
    "Q9s",
    "A3s",
    "A2s",
    # Tier 6: Speculative (top ~40%)
    "98s",
    "ATo",
    "T8s",
    "44",
    "J8s",
    "87s",
    "QTo",
    "K8s",
    "JTo",
    "33",
    "97s",
    "K7s",
    "76s",
    "22",
    "Q8s",
    "K6s",
    "86s",
    "65s",
    "K5s",
    # Tier 7: Weak (top ~60%)
    "54s",
    "J7s",
    "T7s",
    "K4s",
    "Q7s",
    "75s",
    "96s",
    "K3s",
    "J6s",
    "T6s",
    "K2s",
    "Q6s",
    "64s",
    "85s",
    "53s",
    "Q5s",
    "43s",
    "J5s",
    "Q4s",
    "74s",
    "T5s",
    "Q3s",
    "Q2s",
    # Tier 8: Junk (bottom ~40%)
    "A9o",
    "J4s",
    "95s",
    "63s",
    "T4s",
    "J3s",
    "52s",
    "84s",
    "42s",
    "J2s",
    "T3s",
    "93s",
    "73s",
    "T2s",
    "94s",
    "A8o",
    "32s",
    "92s",
    "83s",
    "82s",
    "62s",
    "72s",
    "K9o",
    "A7o",
    "Q9o",
    "A6o",
    "K8o",
    "A5o",
    "J9o",
    "A4o",
    "A3o",
    "K7o",
    "A2o",
    "T9o",
    "Q8o",
    "K6o",
    "98o",
    "J8o",
    "K5o",
    "87o",
    "K4o",
    "T8o",
    "76o",
    "K3o",
    "Q7o",
    "K2o",
    "97o",
    "65o",
    "86o",
    "J7o",
    "Q6o",
    "54o",
    "75o",
    "T7o",
    "Q5o",
    "96o",
    "Q4o",
    "64o",
    "85o",
    "J6o",
    "Q3o",
    "53o",
    "Q2o",
    "J5o",
    "43o",
    "74o",
    "T6o",
    "J4o",
    "J3o",
    "95o",
    "52o",
    "J2o",
    "T5o",
    "63o",
    "84o",
    "T4o",
    "42o",
    "T3o",
    "73o",
    "T2o",
    "93o",
    "32o",
    "94o",
    "92o",
    "83o",
    "82o",
    "62o",
    "72o",
]


@dataclass
class OpponentRange:
    """Represents a distribution of hands an opponent might hold.

    hand_weights maps canonical hand keys (e.g., 'AKs') to weights
    between 0.0 and 1.0 indicating how likely the opponent holds
    that hand.
    """

    hand_weights: dict[str, float] = field(default_factory=dict)

    @classmethod
    def tight(cls) -> OpponentRange:
        """Top ~15% of hands — a tight, solid player."""
        cutoff = int(len(_HAND_TIERS) * 0.15)
        weights = {}
        for i, hand in enumerate(_HAND_TIERS):
            if i < cutoff:
                weights[hand] = 1.0
        return cls(hand_weights=weights)

    @classmethod
    def loose(cls) -> OpponentRange:
        """Top ~50% of hands — a loose, active player."""
        cutoff = int(len(_HAND_TIERS) * 0.50)
        weights = {}
        for i, hand in enumerate(_HAND_TIERS):
            if i < cutoff:
                weights[hand] = 1.0
        return cls(hand_weights=weights)

    @classmethod
    def from_vpip(cls, vpip: float) -> OpponentRange:
        """Estimate a range from VPIP (voluntarily put in pot) percentage.

        VPIP of 0.15 means the player plays ~15% of hands, etc.
        Values are clamped to [0.0, 1.0].

        Args:
            vpip: Float between 0.0 and 1.0 representing the fraction
                  of hands the opponent voluntarily plays.
        """
        vpip = max(0.0, min(1.0, vpip))
        cutoff = int(len(_HAND_TIERS) * vpip)
        weights: dict[str, float] = {}
        for i, hand in enumerate(_HAND_TIERS):
            if i < cutoff:
                weights[hand] = 1.0
            elif i == cutoff:
                # Fractional weight for the boundary hand
                frac = (len(_HAND_TIERS) * vpip) - cutoff
                if frac > 0:
                    weights[hand] = round(frac, 3)
        return cls(hand_weights=weights)

    @property
    def num_hands(self) -> int:
        """Number of hands with nonzero weight."""
        return sum(1 for w in self.hand_weights.values() if w > 0)

    @property
    def total_weight(self) -> float:
        """Sum of all hand weights."""
        return sum(self.hand_weights.values())

    def contains(self, hand_key: str) -> bool:
        """Check if a hand is in this range."""
        return self.hand_weights.get(hand_key, 0.0) > 0.0
