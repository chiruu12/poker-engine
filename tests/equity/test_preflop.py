"""Tests for preflop equity lookup table."""

from poker_engine.core.cards import Card, Suit
from poker_engine.equity.preflop import PREFLOP_EQUITY, hand_key, lookup_preflop_equity


class TestHandKey:
    def test_pocket_pair(self) -> None:
        c1 = Card(rank=14, suit=Suit.SPADES)
        c2 = Card(rank=14, suit=Suit.HEARTS)
        assert hand_key(c1, c2) == "AA"

    def test_suited_higher_first(self) -> None:
        c1 = Card(rank=14, suit=Suit.SPADES)
        c2 = Card(rank=13, suit=Suit.SPADES)
        assert hand_key(c1, c2) == "AKs"

    def test_suited_lower_first_still_canonical(self) -> None:
        c1 = Card(rank=13, suit=Suit.HEARTS)
        c2 = Card(rank=14, suit=Suit.HEARTS)
        assert hand_key(c1, c2) == "AKs"

    def test_offsuit(self) -> None:
        c1 = Card(rank=14, suit=Suit.SPADES)
        c2 = Card(rank=13, suit=Suit.HEARTS)
        assert hand_key(c1, c2) == "AKo"

    def test_low_offsuit(self) -> None:
        c1 = Card(rank=7, suit=Suit.DIAMONDS)
        c2 = Card(rank=2, suit=Suit.CLUBS)
        assert hand_key(c1, c2) == "72o"

    def test_tens(self) -> None:
        c1 = Card(rank=10, suit=Suit.SPADES)
        c2 = Card(rank=10, suit=Suit.HEARTS)
        assert hand_key(c1, c2) == "TT"


class TestLookupPreflopEquity:
    def test_known_hand_aa_vs_1(self) -> None:
        cards = [Card(rank=14, suit=Suit.SPADES), Card(rank=14, suit=Suit.HEARTS)]
        result = lookup_preflop_equity(cards, 1)
        assert result == 0.852

    def test_known_hand_aa_vs_5(self) -> None:
        cards = [Card(rank=14, suit=Suit.SPADES), Card(rank=14, suit=Suit.HEARTS)]
        result = lookup_preflop_equity(cards, 5)
        assert result == 0.495

    def test_known_hand_72o(self) -> None:
        cards = [Card(rank=7, suit=Suit.DIAMONDS), Card(rank=2, suit=Suit.CLUBS)]
        result = lookup_preflop_equity(cards, 1)
        assert result == 0.345

    def test_unknown_hand_returns_none(self) -> None:
        # 94o is not in the table
        cards = [Card(rank=9, suit=Suit.SPADES), Card(rank=4, suit=Suit.HEARTS)]
        result = lookup_preflop_equity(cards, 1)
        assert result is None

    def test_unknown_opponent_count_returns_none(self) -> None:
        cards = [Card(rank=14, suit=Suit.SPADES), Card(rank=14, suit=Suit.HEARTS)]
        result = lookup_preflop_equity(cards, 9)
        assert result is None

    def test_wrong_card_count_returns_none(self) -> None:
        cards = [Card(rank=14, suit=Suit.SPADES)]
        result = lookup_preflop_equity(cards, 1)
        assert result is None

    def test_aks_suited(self) -> None:
        cards = [Card(rank=14, suit=Suit.SPADES), Card(rank=13, suit=Suit.SPADES)]
        result = lookup_preflop_equity(cards, 1)
        assert result == 0.670


class TestPreflopTable:
    def test_has_at_least_25_hands(self) -> None:
        assert len(PREFLOP_EQUITY) >= 25

    def test_all_equities_between_0_and_1(self) -> None:
        for hand, opponents in PREFLOP_EQUITY.items():
            for n, eq in opponents.items():
                assert 0.0 < eq < 1.0, f"{hand} vs {n}: {eq}"

    def test_equity_decreases_with_opponents(self) -> None:
        """More opponents should generally mean lower equity."""
        for hand, opponents in PREFLOP_EQUITY.items():
            sorted_keys = sorted(opponents.keys())
            for i in range(len(sorted_keys) - 1):
                eq_fewer = opponents[sorted_keys[i]]
                eq_more = opponents[sorted_keys[i + 1]]
                assert eq_fewer >= eq_more, (
                    f"{hand}: equity vs {sorted_keys[i]} ({eq_fewer}) "
                    f"< equity vs {sorted_keys[i + 1]} ({eq_more})"
                )
