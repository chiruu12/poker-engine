# Pokertable — Running Commands

## TUI (Graphic Dashboard)

```bash
# Full dashboard with poker table, actions panel, agent thoughts, chip bars
uv run python tmp-playground/run_tui.py
```

## Console Display (Scrolling Log)

```bash
# Inline Rich output — hand-by-hand with colored actions
uv run python tmp-playground/run_table.py
```

## CLI Commands

```bash
# Quick tournament — 4 random bots, 10 hands
uv run python -m poker_engine.cli quick --players 4 --seed 42 --hands 10

# 6-player tournament
uv run python -m poker_engine.cli quick --players 6 --seed 99 --hands 20

# Equity calculator
uv run python -m poker_engine.cli equity As Kh --opponents 2
uv run python -m poker_engine.cli equity AcAd --opponents 1 --simulations 5000
uv run python -m poker_engine.cli equity 7s 2d --opponents 5

# Concatenated card input also works
uv run python -m poker_engine.cli equity AsKh --opponents 3

# CLI help
uv run python -m poker_engine.cli --help
uv run python -m poker_engine.cli quick --help
uv run python -m poker_engine.cli equity --help
```

## Tight Table (Longer Games)

```bash
# Passive bots that check/call more — shows full flop/turn/river
uv run python tmp-playground/run_tight_table.py
```
