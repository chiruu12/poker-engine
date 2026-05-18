# Poker Engine

Pure Texas Hold'em engine with Monte Carlo equity calculator. Zero dependencies. Designed for AI agents.

```python
from poker_engine import PokerEngine, Action, ActionType

engine = PokerEngine(["Alice", "Bob", "Charlie"], starting_chips=1000, seed=42)
engine.new_hand()

# Get valid actions for current player
player = engine.get_current_player()
actions = engine.get_valid_actions(player.name)

# Apply an action
result = engine.apply_action(player.name, Action(ActionType.CALL, 20))

# Check equity
from poker_engine import calculate_equity
equity = calculate_equity(player.hole_cards, engine.community, num_opponents=2)
print(f"Win probability: {equity.win_probability:.0%}")
```

## Installation

```bash
pip install poker-engine
```

## Features

- Complete Texas Hold'em rules (pre-flop through showdown)
- Proper side pots for multi-player all-ins
- Correct betting round termination (raise resets action)
- Dealer button rotation with heads-up special rules
- Monte Carlo equity calculator (~500 simulations, <100ms)
- Hand evaluation for all 10 poker hand ranks
- Human-readable hand descriptions ("Full House, Kings over Tens")
- Turn-based API designed for AI agent integration
- Seeded RNG for reproducible games
- Zero external dependencies

## Architecture

```
src/poker_engine/
├── cards.py      # Card, Suit, HandRank, evaluate_hand, describe_hand
├── engine.py     # PokerEngine state machine (the core)
├── equity.py     # Monte Carlo win probability calculator
└── __init__.py   # Public API exports
```

The engine is a pure state machine — no I/O, no async, no display logic. You call methods, it returns state. This makes it easy to wrap with any interface: CLI, web, AI agents, etc.

## Usage

### Basic Game Loop

```python
from poker_engine import PokerEngine, Action, ActionType

engine = PokerEngine(["Alice", "Bob"], starting_chips=1000)

while not engine.is_tournament_over():
    engine.new_hand()
    
    while not engine.is_hand_over():
        if engine.is_betting_round_complete():
            if engine.phase.name == "RIVER":
                summary = engine.resolve_showdown()
                break
            engine.advance_phase()
            continue
        
        player = engine.get_current_player()
        if player is None:
            break
        
        actions = engine.get_valid_actions(player.name)
        # Your logic to choose an action here
        chosen = actions[1]  # e.g., call/check
        engine.apply_action(player.name, chosen)
    
    engine.rotate_dealer()
```

### Equity Calculator

```python
from poker_engine import calculate_equity
from poker_engine.cards import Card, Suit

hole = [Card(14, Suit.SPADES), Card(14, Suit.HEARTS)]  # Pocket aces
community = [Card(10, Suit.DIAMONDS), Card(7, Suit.CLUBS), Card(2, Suit.SPADES)]

equity = calculate_equity(hole, community, num_opponents=3, num_simulations=1000)
print(f"Hand: {equity.current_hand}")           # "Pair of As"
print(f"Win: {equity.win_probability:.0%}")      # "~82%"
print(f"Improvements: {equity.hand_improvement}") # {"Pair": 0.45, "Two Pair": 0.12, ...}
```

## Development

```bash
git clone https://github.com/chiruu12/poker-engine.git
cd poker-engine
uv sync --extra dev
uv run pytest
uv run ruff check src tests
```

## License

MIT
