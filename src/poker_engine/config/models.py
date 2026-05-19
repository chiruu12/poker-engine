"""Configuration dataclasses for tournaments, agents, and blind structures."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TournamentConfig:
    """Configuration for a poker tournament."""

    name: str = "Default Tournament"
    max_players: int = 9
    starting_chips: int = 1000
    blind_structure: str = "standard"
    payout_structure: str = "top_3"
    hand_delay: float = 1.0
    seed: int | None = None


@dataclass
class AgentConfig:
    """Configuration for an AI agent player."""

    name: str = ""
    type: str = "random"  # "llm", "random", "human"
    model: str = ""
    provider: str = "anthropic"
    api_key_env: str = ""
    personality: str = ""
    temperature: float = 0.7
    system_prompt: str = ""


@dataclass
class BlindConfig:
    """Configuration for blind level progression."""

    levels: list[dict[str, int]] = field(default_factory=list)
