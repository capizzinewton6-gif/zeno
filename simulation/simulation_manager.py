"""Controls virtual execution sandboxes and timeout boundaries."""
from __future__ import annotations

import os
import signal
import subprocess
from dataclasses import dataclass, field
from typing import Any

from ai_core.safety_layer import SafetyLayer
from config import get_settings


@dataclass
class SandboxConfig:
    backend: str = "subprocess"  # subprocess, docker, firejail, wasm
    timeout_seconds: int = 30
    memory_limit_mb: int = 512
    cpu_limit_percent: int = 80
    network: bool = False
    env: dict[str, str] = field(default_factory=dict)


@dataclass
class SandboxResult:
    ok: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool = False
    backend: str = "subprocess"


class SimulationManager:
    """Manages virtual execution sandboxes with timeout/resource boundaries."""

    def __init__(self, config: SandboxConfig | None = None,
                 safety: SafetyLayer | None = None) -> None:
        cfg = get_settings().get("sandbox", {})
        self.config = config or SandboxConfig(
            timeout_seconds=cfg.get("timeout_seconds", 30),
        )
        self.safety = safety or SafetyLayer()

    def run(self, command: str, cwd: str | None = None,
            config: SandboxConfig | None = None) -> SandboxResult:
        cfg = config or self.config
        decision = self.safety.check_command(command)
        if not decision:
            return SandboxResult(False, -1, "", decision.reason, 0, backend=cfg.backend)

        backend = self._select_backend(cfg)
        return backend(command, cwd, cfg)

    def _select_backend(self, cfg: SandboxConfig):
        if cfg.backend == "docker" and self._has("docker"):
            return self._run_docker
        if cfg.backend == "firejail" and self._has("firejail"):
            return self._run_firejail
        return self._run_subprocess

    def _run_subprocess(self, command: str, cwd: str | None,
                        cfg: SandboxConfig) -> SandboxResult:
        import time
        start = time.perf_counter()
        env = os.environ.copy()
        if not cfg.network:
            env["no_proxy"] = "*"
        env.update(cfg.env)
        try:
            proc = subprocess.run(command, shell=True, cwd=cwd, capture_output=True,
                                  text=True, timeout=cfg.timeout_seconds, env=env)
            return SandboxResult(True, proc.returncode, proc.stdout, proc.stderr,
                                 (time.perf_counter() - start) * 1000,
                                 backend="subprocess")
        except subprocess.TimeoutExpired:
            return SandboxResult(False, -1, "", "sandbox timeout",
                                 cfg.timeout_seconds * 1000, timed_out=True,
                                 backend="subprocess")
        except Exception as exc:
            return SandboxResult(False, -1, "", str(exc),
                                 (time.perf_counter() - start) * 1000,
                                 backend="subprocess")

    def _run_docker(self, command: str, cwd: str | None,
                    cfg: SandboxConfig) -> SandboxResult:  # pragma: no cover
        network = "--network=none" if not cfg.network else ""
        mem = f"--memory={cfg.memory_limit_mb}m"
        wrapped = (
            f"docker run --rm {network} {mem} "
            f"--cpus={cfg.cpu_limit_percent / 100} "
            f"-v {cwd or os.getcwd()}:/workspace -w /workspace "
            f"python:3.13-slim sh -c {repr(command)}"
        )
        return self._run_subprocess(wrapped, None, cfg.__class__(backend="subprocess",
                                                                  timeout_seconds=cfg.timeout_seconds))

    def _run_firejail(self, command: str, cwd: str | None,
                      cfg: SandboxConfig) -> SandboxResult:  # pragma: no cover
        net = "--net=none" if not cfg.network else ""
        wrapped = f"firejail {net} --timeout={cfg.timeout_seconds} {command}"
        return self._run_subprocess(wrapped, cwd, cfg.__class__(backend="subprocess",
                                                                timeout_seconds=cfg.timeout_seconds))

    def _has(self, tool: str) -> bool:
        from config import tool_path
        return tool_path(tool) is not None
