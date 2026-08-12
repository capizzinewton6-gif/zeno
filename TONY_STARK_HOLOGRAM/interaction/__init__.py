"""interaction package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .gaze_tracking import GazeTracking
from .multimodal_input import MultimodalInput
from .object_deformation import ObjectDeformation
from .object_manipulator import ObjectManipulator
from .proximity_detector import ProximityDetector
from .spatial_audio import SpatialAudio
from .virtual_buttons import VirtualButtons
from .virtual_keyboard import VirtualKeyboard
from .voice_interface import VoiceInterface


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "gaze_tracking",
        "multimodal_input",
        "object_deformation",
        "object_manipulator",
        "proximity_detector",
        "spatial_audio",
        "virtual_buttons",
        "virtual_keyboard",
        "voice_interface",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("gaze_tracking", GazeTracking),
            ("multimodal_input", MultimodalInput),
            ("object_deformation", ObjectDeformation),
            ("object_manipulator", ObjectManipulator),
            ("proximity_detector", ProximityDetector),
            ("spatial_audio", SpatialAudio),
            ("virtual_buttons", VirtualButtons),
            ("virtual_keyboard", VirtualKeyboard),
            ("voice_interface", VoiceInterface),
        )
    }


__all__ = ["list_modules", "instantiate_all", "GazeTracking", "MultimodalInput", "ObjectDeformation", "ObjectManipulator", "ProximityDetector", "SpatialAudio", "VirtualButtons", "VirtualKeyboard", "VoiceInterface"]
