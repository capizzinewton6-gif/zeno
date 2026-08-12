"""Re-export of the digit-prefixed ``3d_cuboids`` module (importable name)."""

from __future__ import annotations

import importlib.util
import os
import sys

_SPEC = importlib.util.spec_from_file_location(
    "modeling.three_d_cuboids_impl",
    os.path.join(os.path.dirname(__file__), "3d_cuboids.py"),
)
assert _SPEC is not None and _SPEC.loader is not None
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

Cuboid3D = _MODULE.Cuboid3D
cuboid_from_2d = _MODULE.cuboid_from_2d

__all__ = ["Cuboid3D", "cuboid_from_2d"]
