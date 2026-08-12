"""Automated test execution against generated code patches."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capabilities.terminal_execution import CommandResult, TerminalExecution
from simulation.simulation_manager import SandboxConfig, SimulationManager


@dataclass
class RegressionResult:
    total: int = 0
    passed: int = 0
    failed: int = 0
    errors: list[str] = field(default_factory=list)
    duration_ms: float = 0.0

    @property
    def pass_rate(self) -> float:
        return (self.passed / self.total * 100) if self.total else 0.0


class RegressionTester:
    """Runs test suites against patched code and reports results."""

    def __init__(self, simulation: SimulationManager | None = None,
                 terminal: TerminalExecution | None = None) -> None:
        self.simulation = simulation or SimulationManager()
        self.terminal = terminal or TerminalExecution()

    def run_pytest(self, test_path: str = "tests/") -> RegressionResult:
        result = self.simulation.run(
            f"python3 -m pytest {test_path} -v --tb=short",
            config=SandboxConfig(timeout_seconds=120),
        )
        return self._parse_pytest(result)

    def run_jest(self, test_path: str = "") -> RegressionResult:
        cmd = "npx jest" + (f" {test_path}" if test_path else "")
        result = self.simulation.run(cmd, config=SandboxConfig(timeout_seconds=120))
        return self._parse_jest(result)

    def _parse_pytest(self, result: Any) -> RegressionResult:
        out = f"{result.stdout}\n{result.stderr}"
        passed = sum(1 for l in out.splitlines() if " PASSED" in l)
        failed = sum(1 for l in out.splitlines() if " FAILED" in l)
        errors = [l for l in out.splitlines() if "ERROR" in l or "FAILED" in l]
        return RegressionResult(total=passed + failed, passed=passed,
                                 failed=failed, errors=errors[:20],
                                 duration_ms=result.duration_ms)

    def _parse_jest(self, result: Any) -> RegressionResult:
        out = result.stdout
        import re
        pass_m = re.search(r"(\d+)\s+passed", out)
        fail_m = re.search(r"(\d+)\s+failed", out)
        passed = int(pass_m.group(1)) if pass_m else 0
        failed = int(fail_m.group(1)) if fail_m else 0
        return RegressionResult(total=passed + failed, passed=passed,
                                 failed=failed,
                                 errors=[l for l in out.splitlines() if "✕" in l or "FAIL" in l][:20],
                                 duration_ms=result.duration_ms)
