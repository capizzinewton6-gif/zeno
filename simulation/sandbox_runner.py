"""Containerized execution environment (Docker / Wasm / Firejail).

Thin specialization over SimulationManager exposing a sandbox runner interface.
"""
from __future__ import annotations

from dataclasses import dataclass
from simulation.simulation_manager import (
    SandboxConfig, SandboxResult, SimulationManager,
)


class SandboxRunner:
    """High-level sandboxed execution facade."""

    def __init__(self, manager: SimulationManager | None = None) -> None:
        self.manager = manager or SimulationManager()

    def run_python(self, code: str, timeout: int = 30) -> SandboxResult:
        return self.manager.run(f"python3 -c {repr(code)}",
                                config=SandboxConfig(timeout_seconds=timeout, backend="subprocess"))

    def run_script(self, path: str, runner: str = "python3",
                   timeout: int = 30) -> SandboxResult:
        return self.manager.run(f"{runner} {path}",
                                config=SandboxConfig(timeout_seconds=timeout))

    def run_in_docker(self, command: str, image: str = "python:3.13-slim",
                      timeout: int = 60) -> SandboxResult:  # pragma: no cover
        return self.manager.run(
            f"docker run --rm {image} sh -c {repr(command)}",
            config=SandboxConfig(timeout_seconds=timeout, backend="docker"),
        )
