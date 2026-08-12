"""Agent subsystem: specialized mathematical agents."""
from mathematics_ai.agents.base import BaseAgent, AgentResult
from mathematics_ai.agents.compute_agent import ComputeAgent
from mathematics_ai.agents.prover_agent import ProverAgent
from mathematics_ai.agents.conjecture_agent import ConjectureAgent
from mathematics_ai.agents.research_agent import ResearchAgent
from mathematics_ai.agents.optimization_agent import OptimizationAgent
from mathematics_ai.agents.project_agent import ProjectAgent
from mathematics_ai.agents.math_agent import MathAgent
__all__ = [
    "BaseAgent", "AgentResult", "ComputeAgent", "ProverAgent",
    "ConjectureAgent", "ResearchAgent", "OptimizationAgent",
    "ProjectAgent", "MathAgent",
]
