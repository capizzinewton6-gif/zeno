"""Build physical toy models and effective field theories."""

from __future__ import annotations

import sympy as sp


class PhenomenologicalBuilder:
    """Construct effective Lagrangians and toy models from a keyword spec."""

    @staticmethod
    def effective_lagrangian(model: str) -> str:
        models = {
            "phi4": "L = (1/2)(dm phi)^2 - (1/2) m^2 phi^2 - (lambda/4!) phi^4",
            "qed": "L = psi_bar (i gamma^mu D_mu - m) psi - (1/4) F_{mu nu} F^{mu nu}",
            "ym": "L = -(1/4) Tr(F_{mu nu} F^{mu nu}) + psi_bar (i gamma^mu D_mu - m) psi",
            "maxwell": "L = -(1/4) F_{mu nu} F^{mu nu} - J^mu A_mu",
            "sine_gordon": "L = (1/2)(dm phi)^2 + (m^2/beta^2)(cos(beta phi) - 1)",
            "kdv": "u_t + 6 u u_x + u_{xxx} = 0  (Korteweg-de Vries)",
            "flrw": "ds^2 = -dt^2 + a(t)^2 d x^2  (Einstein-Hilbert + matter + Lambda)",
        }
        key = model.lower().replace("-", "_").replace(" ", "_")
        return models.get(key, f"L_eff for '{model}' not in registry; define (kinetic - potential + interactions).")

    @staticmethod
    def toy_potential(name: str) -> str:
        return {
            "harmonic": "V(x) = (1/2) k x^2",
            "well": "V(x) = -V0 Theta(x) Theta(a - x)",
            "morse": "V(r) = D (1 - exp(-a(r-re)))^2",
            "lennard_jones": "V(r) = 4 eps [(sigma/r)^12 - (sigma/r)^6]",
            "cosmic": "V(phi) = (1/2) m^2 phi^2 + lambda phi^4 / 4! (inflaton toy)",
        }.get(name, f"toy potential '{name}' not registered.")
