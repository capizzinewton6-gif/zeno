"""Multi-step pipeline planner for complex physical derivations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class PipelineStep:
    name: str
    action: Callable[..., Any]
    description: str = ""
    depends_on: list[str] = field(default_factory=list)
    result: Any = None
    done: bool = False


@dataclass
class Pipeline:
    name: str
    steps: list[PipelineStep] = field(default_factory=list)
    inputs: dict[str, Any] = field(default_factory=dict)
    outputs: dict[str, Any] = field(default_factory=dict)

    def add_step(self, name: str, action: Callable, description: str = "", depends_on: list[str] | None = None) -> "Pipeline":
        self.steps.append(PipelineStep(name, action, description, depends_on or []))
        return self

    def run(self, verbose: bool = False) -> dict[str, Any]:
        results: dict[str, Any] = dict(self.inputs)
        for step in self.steps:
            if step.done:
                continue
            # Ensure dependencies ran
            args = {k: results[k] for k in step.depends_on if k in results}
            if verbose:
                print(f"[plan] {step.name}")
            step.result = step.action(**args) if args else step.action()
            results[step.name] = step.result
            step.done = True
        self.outputs = results
        return results


class PlanningEngine:
    """Build execution pipelines from a reasoning trace."""

    @staticmethod
    def from_trace_steps(names: list[str], actions: list[Callable]) -> Pipeline:
        pipe = Pipeline(name="derived_pipeline")
        for i, (n, a) in enumerate(zip(names, actions)):
            deps = [names[i - 1]] if i > 0 else []
            pipe.add_step(n, a, description=f"Step {i+1}: {n}", depends_on=deps)
        return pipe

    @staticmethod
    def standard_solver(steps: list[tuple[str, Callable]]) -> Pipeline:
        """Convenience: list of (name, action) -> executed pipeline."""
        pipe = Pipeline(name="solver")
        for i, (n, a) in enumerate(steps):
            pipe.add_step(n, a, depends_on=[steps[i - 1][0]] if i > 0 else [])
        return pipe


PLANNER = PlanningEngine()
