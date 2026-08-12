"""Planning engine — multi-step synthesis and characterization pipeline planning."""

import logging

logger = logging.getLogger(__name__)


class PlanningEngine:
    """Decomposes a chemistry task into a structured multi-step plan."""

    def __init__(self):
        self.templates = {
            "synthesis": [
                "Define target molecule and key bonds.",
                "Retrosynthetic analysis and precursor selection.",
                "Choose reagents, solvents, and catalysts.",
                "Plan order of addition and conditions (T, atmosphere).",
                "Predict yield and side products.",
                "Design purification (extraction, chromatography, recrystallization).",
                "Plan characterization (NMR, MS, IR, mp).",
            ],
            "characterization": [
                "Select appropriate spectroscopic techniques.",
                "Prepare sample and reference.",
                "Acquire spectra under standardized conditions.",
                "Assign peaks/fragments to structural features.",
                "Compare with reference libraries.",
                "Report purity and structural confirmation.",
            ],
            "optimization": [
                "Identify response variable (yield, ee, purity).",
                "Select factors (T, time, equiv, catalyst loading).",
                "Design experimental matrix (DoE).",
                "Execute and analyze variance.",
                "Determine optimum and robustness.",
            ],
        }

    def plan(self, task, context=None):
        task_lower = (task or "").lower()
        kind = "synthesis"
        for key in self.templates:
            if key in task_lower:
                kind = key
                break
        steps = list(self.templates[kind])
        return {
            "task": task,
            "plan_type": kind,
            "steps": steps,
            "context": context or {},
        }

    def add_template(self, name, steps):
        self.templates[name] = list(steps)
