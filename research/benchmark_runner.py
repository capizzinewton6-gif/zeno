"""Evaluates agent accuracy on HumanEval, MBPP, and SWE-bench."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from capabilities.terminal_execution import TerminalExecution
from simulation.simulation_manager import SandboxConfig, SimulationManager


@dataclass
class BenchmarkTask:
    id: str
    prompt: str
    language: str = "python"
    test_cases: list[dict[str, Any]] = field(default_factory=list)
    expected: Any = None


@dataclass
class BenchmarkResult:
    benchmark: str
    total: int = 0
    passed: int = 0
    failed: int = 0
    pass_rate: float = 0.0
    details: list[dict[str, Any]] = field(default_factory=list)


class BenchmarkRunner:
    """Runs coding benchmarks against an agent's generation capability."""

    def __init__(self, simulation: SimulationManager | None = None) -> None:
        self.simulation = simulation or SimulationManager()

    def run_humaneval(self, tasks: list[BenchmarkTask],
                      generator: Callable[[str], str]) -> BenchmarkResult:
        return self._run(tasks, generator, "HumanEval")

    def run_mbpp(self, tasks: list[BenchmarkTask],
                 generator: Callable[[str], str]) -> BenchmarkResult:
        return self._run(tasks, generator, "MBPP")

    def run_swebench(self, tasks: list[BenchmarkTask],
                     patcher: Callable[[str], str]) -> BenchmarkResult:
        """SWE-bench style: patch generation against issue descriptions."""
        return self._run(tasks, patcher, "SWE-bench")

    def load_humaneval_tasks(self, path: str | Path) -> list[BenchmarkTask]:
        """Load HumanEval-format JSONL."""
        tasks: list[BenchmarkTask] = []
        p = Path(path)
        if not p.exists():
            return tasks
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                d = json.loads(line)
                tasks.append(BenchmarkTask(
                    id=d.get("task_id", ""),
                    prompt=d.get("prompt", ""),
                    test_cases=[{"test": d.get("test", "")}],
                ))
            except json.JSONDecodeError:
                continue
        return tasks

    def _run(self, tasks: list[BenchmarkTask], gen: Callable[[str], str],
             name: str) -> BenchmarkResult:
        result = BenchmarkResult(benchmark=name, total=len(tasks))
        for task in tasks:
            code = gen(task.prompt)
            ok = self._verify(code, task)
            result.details.append({"id": task.id, "passed": ok})
            if ok:
                result.passed += 1
            else:
                result.failed += 1
        result.pass_rate = (result.passed / result.total * 100) if result.total else 0.0
        return result

    def _verify(self, code: str, task: BenchmarkTask) -> bool:
        if not task.test_cases and task.expected is not None:
            # Single expected output
            full = f"{code}\n\nprint({task.prompt.split('def ')[-1].split('(')[0]}())"
        elif task.test_cases:
            test = task.test_cases[0].get("test", "")
            full = f"{code}\n\n{test}\n"
        else:
            full = code
        res = self.simulation.run(f"python3 -c {repr(full)}",
                                  config=SandboxConfig(timeout_seconds=10))
        return res.ok and ("Error" not in res.stderr)
