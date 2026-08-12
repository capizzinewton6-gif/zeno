"""Edge-case input generator for automated fuzzing."""
from __future__ import annotations

import random
import string
from dataclasses import dataclass, field
from typing import Any, Callable

from simulation.simulation_manager import SandboxConfig, SimulationManager


@dataclass
class FuzzCase:
    inputs: list[Any]
    output: str
    crashed: bool = False
    error: str = ""


@dataclass
class FuzzReport:
    total: int = 0
    crashes: int = 0
    errors: int = 0
    cases: list[FuzzCase] = field(default_factory=list)

    @property
    def crash_rate(self) -> float:
        return (self.crashes / self.total * 100) if self.total else 0.0


class FuzzTester:
    """Generates edge-case inputs and observes crashes."""

    EDGE_CASES = [
        "", " ", None, 0, -1, 2**31, 2**63, float("inf"), float("nan"),
        "a" * 10_000, "\x00", "🚀", [], {}, [None], [1] * 1000,
    ]

    def __init__(self, simulation: SimulationManager | None = None) -> None:
        self.simulation = simulation or SimulationManager()

    def fuzz_python_function(self, func: Callable[..., Any], arg_count: int = 1,
                             iterations: int = 100) -> FuzzReport:
        report = FuzzReport()
        for _ in range(iterations):
            args = self._gen_args(arg_count)
            case = FuzzCase(inputs=list(args), output="")
            try:
                result = func(*args)
                case.output = repr(result)[:200]
            except Exception as exc:
                case.error = f"{type(exc).__name__}: {exc}"
                case.crashed = True
                report.crashes += 1
            report.cases.append(case)
            report.total += 1
        return report

    def fuzz_script(self, script: str, input_generator: Callable[[], str],
                    iterations: int = 20) -> FuzzReport:
        report = FuzzReport()
        for _ in range(iterations):
            payload = input_generator()
            result = self.simulation.run(
                f"python3 {script}", config=SandboxConfig(timeout_seconds=10),
            )
            case = FuzzCase(inputs=[payload], output=result.stdout[:200],
                            crashed=not result.ok, error=result.stderr[:200])
            if not result.ok:
                report.crashes += 1
            report.cases.append(case)
            report.total += 1
        return report

    def _gen_args(self, count: int) -> tuple:
        return tuple(random.choice(self.EDGE_CASES) for _ in range(count))
