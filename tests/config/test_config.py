"""Tests for YAML config loading."""

import tempfile
from pathlib import Path

from poker_engine.config.defaults import DEFAULT_AGENT, DEFAULT_TOURNAMENT, TURBO_BLINDS
from poker_engine.config.loader import (
    load_agent_config,
    load_blind_config,
    load_tournament_config,
    load_yaml_file,
)
from poker_engine.config.models import AgentConfig, BlindConfig, TournamentConfig


class TestTournamentConfig:
    def test_default_values(self) -> None:
        cfg = TournamentConfig()
        assert cfg.name == "Default Tournament"
        assert cfg.max_players == 9
        assert cfg.starting_chips == 1000
        assert cfg.blind_structure == "standard"
        assert cfg.payout_structure == "top_3"
        assert cfg.hand_delay == 1.0
        assert cfg.seed is None

    def test_load_from_dict(self) -> None:
        data = {
            "name": "My Tournament",
            "max_players": 6,
            "starting_chips": 2000,
            "seed": 42,
        }
        cfg = load_tournament_config(data)
        assert cfg.name == "My Tournament"
        assert cfg.max_players == 6
        assert cfg.starting_chips == 2000
        assert cfg.seed == 42
        # Defaults preserved for unspecified fields
        assert cfg.blind_structure == "standard"
        assert cfg.hand_delay == 1.0

    def test_load_from_default_dict(self) -> None:
        cfg = load_tournament_config(DEFAULT_TOURNAMENT)
        assert cfg.name == "Default Tournament"
        assert cfg.max_players == 9

    def test_unknown_keys_ignored(self) -> None:
        data = {"name": "Test", "unknown_field": 42, "another": "value"}
        cfg = load_tournament_config(data)
        assert cfg.name == "Test"


class TestAgentConfig:
    def test_default_values(self) -> None:
        cfg = AgentConfig()
        assert cfg.name == ""
        assert cfg.type == "random"
        assert cfg.model == ""
        assert cfg.provider == "anthropic"
        assert cfg.temperature == 0.7

    def test_load_from_dict(self) -> None:
        data = {
            "name": "Claude Bot",
            "type": "llm",
            "model": "claude-sonnet-4-20250514",
            "provider": "anthropic",
            "api_key_env": "ANTHROPIC_API_KEY",
            "personality": "aggressive",
            "temperature": 0.9,
            "system_prompt": "Play aggressively.",
        }
        cfg = load_agent_config(data)
        assert cfg.name == "Claude Bot"
        assert cfg.type == "llm"
        assert cfg.model == "claude-sonnet-4-20250514"
        assert cfg.temperature == 0.9
        assert cfg.system_prompt == "Play aggressively."

    def test_load_from_default_dict(self) -> None:
        cfg = load_agent_config(DEFAULT_AGENT)
        assert cfg.name == "Bot"
        assert cfg.type == "random"


class TestBlindConfig:
    def test_default_empty(self) -> None:
        cfg = BlindConfig()
        assert cfg.levels == []

    def test_load_from_dict(self) -> None:
        data = {
            "levels": [
                {"level": 1, "small_blind": 10, "big_blind": 20, "ante": 0},
                {"level": 2, "small_blind": 25, "big_blind": 50, "ante": 5},
            ],
        }
        cfg = load_blind_config(data)
        assert len(cfg.levels) == 2
        assert cfg.levels[0]["small_blind"] == 10
        assert cfg.levels[1]["ante"] == 5

    def test_load_turbo_defaults(self) -> None:
        cfg = load_blind_config(TURBO_BLINDS)
        assert len(cfg.levels) == 8
        assert cfg.levels[0]["duration_hands"] == 5


class TestLoadYamlFile:
    def test_load_valid_yaml(self) -> None:
        import yaml

        data = {"name": "Test Tournament", "max_players": 4}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(data, f)
            path = f.name

        loaded = load_yaml_file(path)
        assert loaded["name"] == "Test Tournament"
        assert loaded["max_players"] == 4
        Path(path).unlink()

    def test_load_real_config_file(self) -> None:
        """Load one of the actual config files from the configs/ directory."""
        config_dir = Path(__file__).parent.parent.parent / "configs"
        turbo_path = config_dir / "blind_structures" / "turbo.yaml"
        if turbo_path.exists():
            data = load_yaml_file(turbo_path)
            cfg = load_blind_config(data)
            assert len(cfg.levels) == 8

    def test_load_invalid_yaml_raises(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("- item1\n- item2\n")
            path = f.name

        import pytest

        with pytest.raises(ValueError, match="Expected a YAML mapping"):
            load_yaml_file(path)
        Path(path).unlink()


class TestRoundTrip:
    def test_tournament_config_roundtrip(self) -> None:
        """Dict -> TournamentConfig -> verify all fields are preserved."""
        original = {
            "name": "Round Trip",
            "max_players": 6,
            "starting_chips": 1500,
            "blind_structure": "turbo",
            "payout_structure": "top_2",
            "hand_delay": 0.5,
            "seed": 99,
        }
        cfg = load_tournament_config(original)
        assert cfg.name == original["name"]
        assert cfg.max_players == original["max_players"]
        assert cfg.starting_chips == original["starting_chips"]
        assert cfg.blind_structure == original["blind_structure"]
        assert cfg.payout_structure == original["payout_structure"]
        assert cfg.hand_delay == original["hand_delay"]
        assert cfg.seed == original["seed"]
