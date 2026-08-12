"""visualization package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .architecture_renderer import ArchitectureRenderer
from .blueprint_renderer import BlueprintRenderer
from .chart_renderer import ChartRenderer
from .data_visualizer import DataVisualizer
from .diagram_renderer import DiagramRenderer
from .graph_renderer import GraphRenderer
from .holographic_dashboard import HolographicDashboard
from .simulation_visualizer import SimulationVisualizer


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "architecture_renderer",
        "blueprint_renderer",
        "chart_renderer",
        "data_visualizer",
        "diagram_renderer",
        "graph_renderer",
        "holographic_dashboard",
        "simulation_visualizer",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("architecture_renderer", ArchitectureRenderer),
            ("blueprint_renderer", BlueprintRenderer),
            ("chart_renderer", ChartRenderer),
            ("data_visualizer", DataVisualizer),
            ("diagram_renderer", DiagramRenderer),
            ("graph_renderer", GraphRenderer),
            ("holographic_dashboard", HolographicDashboard),
            ("simulation_visualizer", SimulationVisualizer),
        )
    }


__all__ = ["list_modules", "instantiate_all", "ArchitectureRenderer", "BlueprintRenderer", "ChartRenderer", "DataVisualizer", "DiagramRenderer", "GraphRenderer", "HolographicDashboard", "SimulationVisualizer"]
