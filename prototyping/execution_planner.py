"""Step-by-step Standard Operating Procedures (SOPs)."""
from __future__ import annotations


class ExecutionPlanner:
    @staticmethod
    def generate_sop(steps: list[dict]) -> dict:
        """Format a list of operations into a numbered SOP."""
        sop = []
        for i, step in enumerate(steps, 1):
            entry = {"step": i, "action": step.get("action", ""),
                     "duration_min": step.get("duration_min", 0),
                     "safety": step.get("safety", ""),
                     "notes": step.get("notes", "")}
            sop.append(entry)
        total = sum(s["duration_min"] for s in steps)
        return {"n_steps": len(sop), "total_duration_min": total, "sop": sop}

    @staticmethod
    def critical_control_points(steps: list[dict]) -> list[dict]:
        return [s for s in steps if s.get("critical")]

    @staticmethod
    def time_estimate(steps: list[dict], buffer_pct: float = 10.0) -> float:
        total = sum(s.get("duration_min", 0) for s in steps)
        return round(total * (1 + buffer_pct / 100), 1)
