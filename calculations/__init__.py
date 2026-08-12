"""Calculation capabilities (One Capability = One Module)."""

from .engineering_math import EngineeringMath
from .mechanics import Mechanics, GRAVITY
from .electricity import Electricity
from .thermodynamics import Thermodynamics, R_UNIVERSAL
from .fluid_mechanics import FluidMechanics
from .structural import Structural
from .circuits import Circuits
from .unit_converter import UnitConverter

__all__ = [
    "EngineeringMath", "Mechanics", "GRAVITY", "Electricity",
    "Thermodynamics", "R_UNIVERSAL", "FluidMechanics", "Structural",
    "Circuits", "UnitConverter",
]
