"""Design capabilities (One Capability = One Module)."""

from .cad_manager import CADManager, CADProject
from .design_2d import Design2D
from .design_3d import Design3D
from .technical_drawing import TechnicalDrawing
from .dimensioning import Dimensioning, DEFAULT_TOLERANCES
from .materials import DesignMaterials
from .design_rules import DesignRules, DESIGN_RULES

__all__ = [
    "CADManager", "CADProject", "Design2D", "Design3D", "TechnicalDrawing",
    "Dimensioning", "DEFAULT_TOLERANCES", "DesignMaterials", "DesignRules", "DESIGN_RULES",
]
