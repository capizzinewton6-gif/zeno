"""Main chemical intelligence agent.

Coordinates all chemistry capabilities and routes user requests to the
appropriate specialist agent or capability module.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_core import AIEngine
from ai_core.safety_layer import SafetyLayer
from .synthetic_agent import SyntheticAgent
from .quantum_agent import QuantumAgent
from .analytical_agent import AnalyticalAgent
from .research_agent import ResearchAgent
from .optimization_agent import OptimizationAgent
from .project_agent import ProjectAgent


class ChemistryAgent:
    """Top-level chemistry intelligence orchestrator."""

    def __init__(self, api_key=None):
        self.ai = AIEngine(api_key=api_key)
        self.safety = SafetyLayer()
        self.synthetic = SyntheticAgent(api_key=api_key)
        self.quantum = QuantumAgent(api_key=api_key)
        self.analytical = AnalyticalAgent(api_key=api_key)
        self.research = ResearchAgent(api_key=api_key)
        self.optimization = OptimizationAgent(api_key=api_key)
        self.project = ProjectAgent(api_key=api_key)

    def handle(self, request):
        """Route a user request to the right capability/agent.

        request: dict with 'task' and optional 'params'.
        """
        task = request.get("task", "")
        screen = self.safety.screen(task)
        if screen.get("blocked"):
            return {"agent": "ChemistryAgent", "blocked": True, "response": screen["message"]}

        text = task.lower()
        # Routing heuristics
        if any(k in text for k in ["synthes", "retro", "route", "protecting group", "purif", "scale-up"]):
            result = self.synthetic.handle(request)
        elif any(k in text for k in ["quantum", "dft", "orbital", "basis set", "hamiltonian", "ab initio"]):
            result = self.quantum.handle(request)
        elif any(k in text for k in ["nmr", "ir", "uv", "mass spec", "chromat", "spectr", "titrat",
                                      "beer", "ph", "acid", "buffer", "henderson", "absorbance",
                                      "calibration", "kinetic curve", "spectrum"]):
            result = self.analytical.handle(request)
        elif any(k in text for k in ["search", "literature", "pubchem", "patent", "paper", "reference"]):
            result = self.research.handle(request)
        elif any(k in text for k in ["optimiz", "doe", "yield improve", "stoichiom", "kinetic"]):
            result = self.optimization.handle(request)
        elif any(k in text for k in ["project", "notebook", "milestone", "report", "manuscript"]):
            result = self.project.handle(request)
        else:
            # General reasoning via AI engine
            result = self.ai.deep_reason(task, request.get("params"))

        result.setdefault("agent", "ChemistryAgent")
        result["safety_flags"] = screen
        return result

    def describe(self):
        return {
            "agent": "ChemistryAgent",
            "role": "Main chemical intelligence and routing",
            "specialists": {
                "synthetic": "SyntheticAgent",
                "quantum": "QuantumAgent",
                "analytical": "AnalyticalAgent",
                "research": "ResearchAgent",
                "optimization": "OptimizationAgent",
                "project": "ProjectAgent",
            },
        }
