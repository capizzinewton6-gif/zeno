"""Strict physical unit and dimension consistency verifier."""

from __future__ import annotations

import sympy as sp

from calculations.dimensional_analysis import Dimension, DimensionalAnalysis, BASE_DIMS


class DimensionalValidator:
    """Check that physical equations and expressions are dimensionally consistent."""

    @staticmethod
    def check_equation(left_dim: Dimension, right_dim: Dimension) -> dict:
        ok = DimensionalAnalysis.consistent(left_dim, right_dim)
        return {
            "left": left_dim.as_str(),
            "right": right_dim.as_str(),
            "consistent": ok,
        }

    @staticmethod
    def check_quantity_dimension(quantity: str, expected: Dimension) -> dict:
        actual = DimensionalAnalysis.dim_of(quantity)
        ok = DimensionalAnalysis.consistent(actual, expected)
        return {"quantity": quantity, "actual": actual.as_str(), "expected": expected.as_str(), "consistent": ok}

    @staticmethod
    def check_symbolic_expr(expr: sp.Expr, symbol_dims: dict[sp.Symbol, Dimension]) -> dict:
        """Sum the dimensions of terms; a dimensionally consistent sum has equal dims per term."""
        # Replace each symbol by its dimension exponent vector and check term-wise.
        terms = expr.expand().as_ordered_terms()
        term_dims: list[Dimension] = []
        zero = Dimension({k: 0 for k in BASE_DIMS})
        for term in terms:
            d = Dimension({k: 0 for k in BASE_DIMS})
            for sym, exponent in term.as_powers_dict().items():
                if sym in symbol_dims:
                    sd = symbol_dims[sym]
                    n = int(exponent)
                    d = Dimension({k: d.exponents.get(k, 0) + sd.exponents.get(k, 0) * n for k in BASE_DIMS})
                # numeric coefficients contribute nothing
            term_dims.append(d)
        consistent = all(d.exponents == term_dims[0].exponents for d in term_dims[1:])
        return {
            "n_terms": len(terms),
            "term_dimensions": [d.as_str() for d in term_dims],
            "consistent": consistent,
        }
