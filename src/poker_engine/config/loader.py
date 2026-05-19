"""Load configuration from YAML dicts and files."""

from __future__ import annotations

from pathlib import Path

from poker_engine.config.models import AgentConfig, BlindConfig, TournamentConfig


def load_tournament_config(data: dict) -> TournamentConfig:
    """Create a TournamentConfig from a dict (e.g., parsed YAML).

    Unknown keys are silently ignored.
    """
    fields = {f.name for f in TournamentConfig.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in fields}
    return TournamentConfig(**filtered)


def load_agent_config(data: dict) -> AgentConfig:
    """Create an AgentConfig from a dict (e.g., parsed YAML).

    Unknown keys are silently ignored.
    """
    fields = {f.name for f in AgentConfig.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in fields}
    return AgentConfig(**filtered)


def load_blind_config(data: dict) -> BlindConfig:
    """Create a BlindConfig from a dict (e.g., parsed YAML).

    Unknown keys are silently ignored.
    """
    fields = {f.name for f in BlindConfig.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in fields}
    return BlindConfig(**filtered)


def load_yaml_file(path: str | Path) -> dict:
    """Load a YAML file and return its contents as a dict.

    Requires pyyaml to be installed. The import is deferred so that
    pyyaml is not a hard dependency of the core package.
    """
    import yaml

    filepath = Path(path)
    with filepath.open("r") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected a YAML mapping at top level, got {type(data).__name__}")
    return data
