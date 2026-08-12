"""spatial_computing package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .boundary_manager import BoundaryManager
from .multi_room_sync import MultiRoomSync
from .obstacle_detector import ObstacleDetector
from .occlusion_engine import OcclusionEngine
from .physics_grounding import PhysicsGrounding
from .room_persistence import RoomPersistence
from .room_scanner import RoomScanner
from .spatial_anchor_manager import SpatialAnchorManager
from .spatial_mapper import SpatialMapper
from .surface_anchor import SurfaceAnchor


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "boundary_manager",
        "multi_room_sync",
        "obstacle_detector",
        "occlusion_engine",
        "physics_grounding",
        "room_persistence",
        "room_scanner",
        "spatial_anchor_manager",
        "spatial_mapper",
        "surface_anchor",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("boundary_manager", BoundaryManager),
            ("multi_room_sync", MultiRoomSync),
            ("obstacle_detector", ObstacleDetector),
            ("occlusion_engine", OcclusionEngine),
            ("physics_grounding", PhysicsGrounding),
            ("room_persistence", RoomPersistence),
            ("room_scanner", RoomScanner),
            ("spatial_anchor_manager", SpatialAnchorManager),
            ("spatial_mapper", SpatialMapper),
            ("surface_anchor", SurfaceAnchor),
        )
    }


__all__ = ["list_modules", "instantiate_all", "BoundaryManager", "MultiRoomSync", "ObstacleDetector", "OcclusionEngine", "PhysicsGrounding", "RoomPersistence", "RoomScanner", "SpatialAnchorManager", "SpatialMapper", "SurfaceAnchor"]
