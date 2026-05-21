# PokerTable

Texas Hold'em engine with LLM agent tournaments, poker tools, CLI commands, and Rich terminal displays. Designed for agent frameworks, but usable as a plain game engine.

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
pip install pokertable
```

## Features

- Complete Texas Hold'em rules (pre-flop through showdown)
- Proper side pots for multi-player all-ins
- Correct betting round termination (raise resets action)
- Dealer button rotation with heads-up special rules
- Monte Carlo equity calculator plus preflop/range helpers
- Hand evaluation for all 10 poker hand ranks
- Human-readable hand descriptions ("Full House, Kings over Tens")
- Turn-based API designed for AI agent integration
- Decorator-based poker tools for LLM providers and agent frameworks
- Tournament director, blind schedules, event bus, payouts, and history
- Rich console display and adaptive poker-table TUI
- Seeded RNG for reproducible games

## Architecture

```
src/poker_engine/
├── core/         # PokerEngine state machine, cards, hand evaluation
├── equity/       # Monte Carlo, preflop lookup, ranges, cache
├── tools/        # @tool decorator, schemas, registry, poker toolkits
├── players/      # Human, random, scripted, and LLM player interfaces
├── tournament/   # Director, events, blinds, payout, history, table manager
├── config/       # YAML config models and loader
├── tui/          # Rich table view, console display, action/thought panels
├── cli.py        # `poker` command
└── __init__.py   # Public API exports
```

The core engine stays a pure state machine. The tournament, player, tools, CLI, and TUI layers wrap it without making the rules engine depend on any one provider or framework.

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

### CLI And TUI

```bash
# Quick tournament with random players
poker quick --players 4 --seed 42 --hands 10

# Equity calculator
poker equity As Kh --opponents 3

# From a source checkout: graphical poker table demo
uv run python tmp-playground/run_tui.py

# From a source checkout: scrolling console demo
uv run python tmp-playground/run_table.py

# From a source checkout: real-model TUI demo
uv run python tmp-playground/run_real_tui.py
```

The importable displays are available as:

```python
from poker_engine.tui import ConsoleDisplay, PokerTUI
```

## Development

```bash
git clone https://github.com/chiruu12/pokertable.git
cd pokertable
uv sync --extra dev
uv run pytest
uv run ruff check src tests
```

## License

MIT
