"""rendering package - auto-registers its capability modules."""

from typing import Any, Dict, List

# Per-module imports (kept explicit so a failing import does not break
# the whole package).
from .fft_engine import FftEngine
from .gaussian_splat_renderer import GaussianSplatRenderer
from .gpu_acceleration import GpuAcceleration
from .lod_manager import LodManager
from .occlusion_culling import OcclusionCulling
from .point_cloud_renderer import PointCloudRenderer
from .ray_tracing import RayTracing
from .render_engine import RenderEngine


def list_modules() -> List[str]:
    """Return the capability names registered in this package."""
    return [
        "fft_engine",
        "gaussian_splat_renderer",
        "gpu_acceleration",
        "lod_manager",
        "occlusion_culling",
        "point_cloud_renderer",
        "ray_tracing",
        "render_engine",
    ]


def instantiate_all(config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Instantiate every module in this package and return name->instance."""
    return {
        name: cls(config=config)
        for name, cls in (
            ("fft_engine", FftEngine),
            ("gaussian_splat_renderer", GaussianSplatRenderer),
            ("gpu_acceleration", GpuAcceleration),
            ("lod_manager", LodManager),
            ("occlusion_culling", OcclusionCulling),
            ("point_cloud_renderer", PointCloudRenderer),
            ("ray_tracing", RayTracing),
            ("render_engine", RenderEngine),
        )
    }


__all__ = ["list_modules", "instantiate_all", "FftEngine", "GaussianSplatRenderer", "GpuAcceleration", "LodManager", "OcclusionCulling", "PointCloudRenderer", "RayTracing", "RenderEngine"]
