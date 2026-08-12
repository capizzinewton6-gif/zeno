"""holographic_objects package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .animation_controller import AnimationController
from .exploded_view import ExplodedView
from .measurement_tools import MeasurementTools
from .model_converter import ModelConverter
from .model_loader import ModelLoader
from .object_library import ObjectLibrary
from .object_manager import ObjectManager
from .object_transform import ObjectTransform


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "animation_controller",
        "exploded_view",
        "measurement_tools",
        "model_converter",
        "model_loader",
        "object_library",
        "object_manager",
        "object_transform",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("animation_controller", AnimationController),
            ("exploded_view", ExplodedView),
            ("measurement_tools", MeasurementTools),
            ("model_converter", ModelConverter),
            ("model_loader", ModelLoader),
            ("object_library", ObjectLibrary),
            ("object_manager", ObjectManager),
            ("object_transform", ObjectTransform),
        )
    }


__all__ = ["list_modules", "instantiate_all", "AnimationController", "ExplodedView", "MeasurementTools", "ModelConverter", "ModelLoader", "ObjectLibrary", "ObjectManager", "ObjectTransform"]
