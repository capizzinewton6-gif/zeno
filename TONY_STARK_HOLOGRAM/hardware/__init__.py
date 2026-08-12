"""hardware package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .camera_manager import CameraManager
from .depth_camera import DepthCamera
from .optical_calibration import OpticalCalibration
from .projector_controller import ProjectorController
from .safety_interlock import SafetyInterlock
from .sensor_manager import SensorManager
from .spatial_light_modulator import SpatialLightModulator
from .thermal_manager import ThermalManager


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "camera_manager",
        "depth_camera",
        "optical_calibration",
        "projector_controller",
        "safety_interlock",
        "sensor_manager",
        "spatial_light_modulator",
        "thermal_manager",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("camera_manager", CameraManager),
            ("depth_camera", DepthCamera),
            ("optical_calibration", OpticalCalibration),
            ("projector_controller", ProjectorController),
            ("safety_interlock", SafetyInterlock),
            ("sensor_manager", SensorManager),
            ("spatial_light_modulator", SpatialLightModulator),
            ("thermal_manager", ThermalManager),
        )
    }


__all__ = ["list_modules", "instantiate_all", "CameraManager", "DepthCamera", "OpticalCalibration", "ProjectorController", "SafetyInterlock", "SensorManager", "SpatialLightModulator", "ThermalManager"]
