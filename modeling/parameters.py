"""Variables, fields, boundary conditions, and gauge choices."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class Parameter:
    name: str
    value: float
    unit: str = "SI"
    bounds: tuple[float, float] | None = None
    description: str = ""


@dataclass
class BoundaryCondition:
    kind: str  # dirichlet | neumann | periodic | robin
    location: str
    value: Any = 0.0


@dataclass
class FieldVariable:
    name: str
    symbol: str
    dimensions: str
    description: str = ""


class Parameters:
    """Manage physical parameters, fields, and boundary conditions."""

    def __init__(self):
        self.params: dict[str, Parameter] = {}
        self.fields: dict[str, FieldVariable] = {}
        self.bcs: list[BoundaryCondition] = []
        self.gauge: str = "lorentz"

    def add_param(self, p: Parameter) -> None:
        self.params[p.name] = p

    def add_field(self, f: FieldVariable) -> None:
        self.fields[f.name] = f

    def add_bc(self, bc: BoundaryCondition) -> None:
        self.bcs.append(bc)

    def set_gauge(self, gauge: str) -> None:
        self.gauge = gauge

    def snapshot(self) -> dict:
        return {
            "parameters": {k: v.__dict__ for k, v in self.params.items()},
            "fields": {k: v.__dict__ for k, v in self.fields.items()},
            "boundary_conditions": [b.__dict__ for b in self.bcs],
            "gauge": self.gauge,
        }
