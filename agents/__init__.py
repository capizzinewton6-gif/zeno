"""Autonomous agents (One Capability = One Module).

These agents orchestrate the capability modules and AI engines.
"""

from .engineering_agent import EngineeringAgent
from .inventor_agent import InventorAgent
from .design_agent import DesignAgent
from .simulation_agent import SimulationAgent
from .research_agent import ResearchAgent
from .optimization_agent import OptimizationAgent
from .project_agent import ProjectAgent

__all__ = [
    "EngineeringAgent", "InventorAgent", "DesignAgent", "SimulationAgent",
    "ResearchAgent", "OptimizationAgent", "ProjectAgent",
]
