"""scientific_visualization package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .anatomy_viewer import AnatomyViewer
from .biology_visualizer import BiologyVisualizer
from .chemistry_visualizer import ChemistryVisualizer
from .equation_visualizer import EquationVisualizer
from .molecular_viewer import MolecularViewer
from .physics_visualizer import PhysicsVisualizer
from .simulation_viewer import SimulationViewer


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "anatomy_viewer",
        "biology_visualizer",
        "chemistry_visualizer",
        "equation_visualizer",
        "molecular_viewer",
        "physics_visualizer",
        "simulation_viewer",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("anatomy_viewer", AnatomyViewer),
            ("biology_visualizer", BiologyVisualizer),
            ("chemistry_visualizer", ChemistryVisualizer),
            ("equation_visualizer", EquationVisualizer),
            ("molecular_viewer", MolecularViewer),
            ("physics_visualizer", PhysicsVisualizer),
            ("simulation_viewer", SimulationViewer),
        )
    }


__all__ = ["list_modules", "instantiate_all", "AnatomyViewer", "BiologyVisualizer", "ChemistryVisualizer", "EquationVisualizer", "MolecularViewer", "PhysicsVisualizer", "SimulationViewer"]
