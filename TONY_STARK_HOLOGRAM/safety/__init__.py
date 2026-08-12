"""safety package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .collision_safety import CollisionSafety
from .emergency_shutdown import EmergencyShutdown
from .eye_safety import EyeSafety
from .hardware_safety import HardwareSafety
from .spatial_safety import SpatialSafety


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "collision_safety",
        "emergency_shutdown",
        "eye_safety",
        "hardware_safety",
        "spatial_safety",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("collision_safety", CollisionSafety),
            ("emergency_shutdown", EmergencyShutdown),
            ("eye_safety", EyeSafety),
            ("hardware_safety", HardwareSafety),
            ("spatial_safety", SpatialSafety),
        )
    }


__all__ = ["list_modules", "instantiate_all", "CollisionSafety", "EmergencyShutdown", "EyeSafety", "HardwareSafety", "SpatialSafety"]
