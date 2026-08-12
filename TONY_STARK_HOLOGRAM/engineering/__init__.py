"""engineering package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .airflow_visualizer import AirflowVisualizer
from .assembly_viewer import AssemblyViewer
from .cad_viewer import CadViewer
from .collision_checker import CollisionChecker
from .component_inspector import ComponentInspector
from .digital_twin import DigitalTwin
from .stress_visualizer import StressVisualizer
from .thermal_visualizer import ThermalVisualizer


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "airflow_visualizer",
        "assembly_viewer",
        "cad_viewer",
        "collision_checker",
        "component_inspector",
        "digital_twin",
        "stress_visualizer",
        "thermal_visualizer",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("airflow_visualizer", AirflowVisualizer),
            ("assembly_viewer", AssemblyViewer),
            ("cad_viewer", CadViewer),
            ("collision_checker", CollisionChecker),
            ("component_inspector", ComponentInspector),
            ("digital_twin", DigitalTwin),
            ("stress_visualizer", StressVisualizer),
            ("thermal_visualizer", ThermalVisualizer),
        )
    }


__all__ = ["list_modules", "instantiate_all", "AirflowVisualizer", "AssemblyViewer", "CadViewer", "CollisionChecker", "ComponentInspector", "DigitalTwin", "StressVisualizer", "ThermalVisualizer"]
