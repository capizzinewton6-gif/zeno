"""Mathematical capability modules: one capability per module.

Each submodule wraps SymPy/NumPy/mpmath to provide real mathematical
computations. The package is imported lazily by the agent layer.
"""

from mathematics_ai.mathematics import (
    algebra, analysis, topology, geometry, number_theory,
    combinatorics, logic, probability, linear_algebra,
)

__all__ = [
    "algebra", "analysis", "topology", "geometry", "number_theory",
    "combinatorics", "logic", "probability", "linear_algebra",
]
