"""Immune response, antibodies, and pathogens."""
from __future__ import annotations

from biology._shared import safe_ai_reason

ISOTYPES = {
    "IgG": "Most abundant serum antibody; opsonization, complement activation, neonatal immunity.",
    "IgM": "First antibody produced; pentameric; efficient complement activator.",
    "IgA": "Mucosal immunity; secreted as dimer across epithelia.",
    "IgE": "Allergy and defense against parasites; binds mast cells/basophils.",
    "IgD": "B-cell receptor; role in B-cell activation.",
}


class ImmunologyModule:
    def handle(self, command: str, query: str, ctx) -> str:
        q = query.lower()
        for iso in ISOTYPES:
            if iso.lower() in q:
                return f"{iso}: {ISOTYPES[iso]}"
        return safe_ai_reason(query, ctx)

    @staticmethod
    def antibody_isotype_info(isotype: str) -> dict:
        key = isotype.strip()
        return {"isotype": key, "function": ISOTYPES.get(key, "Unknown isotype.")}

    @staticmethod
    def binding_affinity_kd(ka: float, kd: float) -> float:
        """Equilibrium dissociation constant Kd = kd / ka."""
        if ka == 0:
            raise ValueError("ka (association rate) must be > 0")
        return kd / ka

    @staticmethod
    def tcr_recognition_affinity(kd: float) -> str:
        if kd <= 1e-6:
            return "high affinity"
        if kd <= 1e-4:
            return "moderate affinity"
        return "low affinity"
