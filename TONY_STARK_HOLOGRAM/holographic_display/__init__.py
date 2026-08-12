"""holographic_display package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .depth_renderer import DepthRenderer
from .display_manager import DisplayManager
from .lightfield_renderer import LightfieldRenderer
from .lighting_engine import LightingEngine
from .material_renderer import MaterialRenderer
from .optical_effects import OpticalEffects
from .parallax_engine import ParallaxEngine
from .shadow_engine import ShadowEngine
from .spatial_renderer import SpatialRenderer
from .transparency_engine import TransparencyEngine
from .volumetric_renderer import VolumetricRenderer


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "depth_renderer",
        "display_manager",
        "lightfield_renderer",
        "lighting_engine",
        "material_renderer",
        "optical_effects",
        "parallax_engine",
        "shadow_engine",
        "spatial_renderer",
        "transparency_engine",
        "volumetric_renderer",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("depth_renderer", DepthRenderer),
            ("display_manager", DisplayManager),
            ("lightfield_renderer", LightfieldRenderer),
            ("lighting_engine", LightingEngine),
            ("material_renderer", MaterialRenderer),
            ("optical_effects", OpticalEffects),
            ("parallax_engine", ParallaxEngine),
            ("shadow_engine", ShadowEngine),
            ("spatial_renderer", SpatialRenderer),
            ("transparency_engine", TransparencyEngine),
            ("volumetric_renderer", VolumetricRenderer),
        )
    }


__all__ = ["list_modules", "instantiate_all", "DepthRenderer", "DisplayManager", "LightfieldRenderer", "LightingEngine", "MaterialRenderer", "OpticalEffects", "ParallaxEngine", "ShadowEngine", "SpatialRenderer", "TransparencyEngine", "VolumetricRenderer"]
