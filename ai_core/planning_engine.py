"""Planning engine: multi-camera pipeline and processing queue planning."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class PlanStep:
    capability: str          # module.function path
    args: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[int] = field(default_factory=list)
    reason: str = ""


@dataclass
class Plan:
    goal: str
    steps: List[PlanStep] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"goal": self.goal,
                "steps": [{"capability": s.capability, "args": s.args,
                           "depends_on": s.depends_on, "reason": s.reason}
                          for s in self.steps]}


class PlanningEngine:
    """Builds an executable plan of capability steps from an LLM-derived intent."""

    def __init__(self) -> None:
        self.capability_registry: Dict[str, str] = {}

    def register(self, intent: str, capability: str) -> None:
        self.capability_registry[intent.lower()] = capability

    def from_intent(self, intent: dict) -> Plan:
        goal = intent.get("goal", "unspecified")
        steps_raw = intent.get("plan") or intent.get("capabilities") or []
        plan = Plan(goal=goal)
        if isinstance(steps_raw, list) and steps_raw and isinstance(steps_raw[0], str):
            # capability list form
            for i, cap in enumerate(steps_raw):
                plan.steps.append(PlanStep(capability=cap, depends_on=[i - 1] if i else []))
        elif isinstance(steps_raw, list):
            for i, s in enumerate(steps_raw):
                if isinstance(s, dict):
                    plan.steps.append(PlanStep(
                        capability=s.get("capability", s.get("name", "")),
                        args=s.get("args", {}),
                        depends_on=s.get("depends_on", [i - 1] if i else []),
                        reason=s.get("reason", ""),
                    ))
        return plan

    def topological_order(self, plan: Plan) -> List[PlanStep]:
        """Return steps in dependency order (simple Kahn's algorithm)."""
        ordered: List[PlanStep] = []
        remaining = list(enumerate(plan.steps))
        done: set = set()
        while remaining:
            progressed = False
            for i, step in list(remaining):
                if all(d in done for d in step.depends_on):
                    ordered.append(step)
                    done.add(i)
                    remaining.remove((i, step))
                    progressed = True
            if not progressed:
                # cycle / missing deps: append the rest in order
                ordered.extend(s for _, s in remaining)
                break
        return ordered
