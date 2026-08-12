"""Biological problem and organism context manager."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class BiologyContext:
    organism: str = "Escherichia coli"
    domain: str = "molecular biology"
    codon_table: str = "Bacterial"
    temperature_c: float = 37.0
    bsl_level: int = 1
    notes: str = ""

    def as_prompt(self) -> str:
        return (
            f"Context: organism={self.organism}; domain={self.domain}; "
            f"codon_table={self.codon_table}; temperature={self.temperature_c}C; "
            f"BSL={self.bsl_level}; notes={self.notes}"
        )


class ContextManager:
    """Holds and updates the active biological context for a session."""

    def __init__(self, ctx: BiologyContext | None = None):
        self.history: list[BiologyContext] = [ctx or BiologyContext()]
        self.entities: dict[str, str] = {}

    @property
    def current(self) -> BiologyContext:
        return self.history[-1]

    def update(self, **kwargs) -> BiologyContext:
        latest = BiologyContext(**{**self.current.__dict__, **kwargs})
        self.history.append(latest)
        return latest

    def register_entity(self, name: str, description: str) -> None:
        self.entities[name] = description

    def context_string(self) -> str:
        return self.current.as_prompt()
