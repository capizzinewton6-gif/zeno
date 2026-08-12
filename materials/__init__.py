"""Materials capabilities (One Capability = One Module)."""

from .material_database import MaterialDatabase, MATERIALS
from .strength import MaterialStrength
from .thermal_properties import ThermalProperties
from .electrical_properties import ElectricalProperties, ELECTRICAL_DATA
from .material_selector import MaterialSelector

__all__ = [
    "MaterialDatabase", "MATERIALS", "MaterialStrength",
    "ThermalProperties", "ElectricalProperties", "ELECTRICAL_DATA", "MaterialSelector",
]
