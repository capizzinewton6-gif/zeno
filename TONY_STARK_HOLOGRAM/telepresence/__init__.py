"""telepresence package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .avatar_renderer import AvatarRenderer
from .point_cloud_stream import PointCloudStream
from .spatial_stream import SpatialStream
from .telepresence_manager import TelepresenceManager
from .volumetric_capture import VolumetricCapture


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "avatar_renderer",
        "point_cloud_stream",
        "spatial_stream",
        "telepresence_manager",
        "volumetric_capture",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("avatar_renderer", AvatarRenderer),
            ("point_cloud_stream", PointCloudStream),
            ("spatial_stream", SpatialStream),
            ("telepresence_manager", TelepresenceManager),
            ("volumetric_capture", VolumetricCapture),
        )
    }


__all__ = ["list_modules", "instantiate_all", "AvatarRenderer", "PointCloudStream", "SpatialStream", "TelepresenceManager", "VolumetricCapture"]
