"""gesture_control package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .air_drawing import AirDrawing
from .gesture_macros import GestureMacros
from .gesture_recognizer import GestureRecognizer
from .hand_tracker import HandTracker
from .pinch_controller import PinchController
from .raycast_controller import RaycastController
from .sensitivity_manager import SensitivityManager
from .skeleton_tracker import SkeletonTracker
from .tremor_filter import TremorFilter
from .two_hand_controller import TwoHandController


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "air_drawing",
        "gesture_macros",
        "gesture_recognizer",
        "hand_tracker",
        "pinch_controller",
        "raycast_controller",
        "sensitivity_manager",
        "skeleton_tracker",
        "tremor_filter",
        "two_hand_controller",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("air_drawing", AirDrawing),
            ("gesture_macros", GestureMacros),
            ("gesture_recognizer", GestureRecognizer),
            ("hand_tracker", HandTracker),
            ("pinch_controller", PinchController),
            ("raycast_controller", RaycastController),
            ("sensitivity_manager", SensitivityManager),
            ("skeleton_tracker", SkeletonTracker),
            ("tremor_filter", TremorFilter),
            ("two_hand_controller", TwoHandController),
        )
    }


__all__ = ["list_modules", "instantiate_all", "AirDrawing", "GestureMacros", "GestureRecognizer", "HandTracker", "PinchController", "RaycastController", "SensitivityManager", "SkeletonTracker", "TremorFilter", "TwoHandController"]
