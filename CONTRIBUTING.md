# Contributing to PokerTable

## Branching Rules

**Never push directly to `main`.** Always create a feature branch and open a PR.

```bash
git checkout -b feat/my-feature   # new feature
git checkout -b fix/bug-name      # bug fix
git checkout -b docs/update       # documentation
git checkout -b ci/improvement    # CI/CD changes
```

Open a PR to `main`, wait for CI to pass, then merge.

## Development Setup

```bash
git clone https://github.com/chiruu12/pokertable.git
cd poker-engine
uv sync --extra dev
```

## Running Checks

```bash
uv run pytest              # tests
uv run ruff check src tests # lint
uv run ruff format src tests # format
```

## Project Structure

```
src/poker_engine/
├── cards.py      # Card, Suit, HandRank, evaluate_hand, describe_hand
├── engine.py     # PokerEngine — pure state machine
├── equity.py     # Monte Carlo equity calculator
└── __init__.py   # Public exports
tests/
├── test_cards.py
├── test_engine.py
└── test_equity.py
```

## Adding Features

- Engine changes must be pure (no I/O, no async)
- All new logic needs tests
- Chips must be conserved (total chips in == total chips out)
- Run `uv run ruff check src tests` before committing

## Pull Request Guidelines

- One logical change per PR
- Tests must pass
- Lint must pass
- Clear description of what changed and why
