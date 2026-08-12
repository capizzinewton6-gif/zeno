"""persistence package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .configuration import Configuration
from .object_state import ObjectState
from .scene_manager import SceneManager
from .spatial_memory import SpatialMemory


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "configuration",
        "object_state",
        "scene_manager",
        "spatial_memory",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("configuration", Configuration),
            ("object_state", ObjectState),
            ("scene_manager", SceneManager),
            ("spatial_memory", SpatialMemory),
        )
    }


__all__ = ["list_modules", "instantiate_all", "Configuration", "ObjectState", "SceneManager", "SpatialMemory"]
