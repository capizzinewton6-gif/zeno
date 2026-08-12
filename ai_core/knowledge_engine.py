"""Physical ontology, conservation laws, and interdisciplinary field graph."""

from __future__ import annotations

from typing import Any


CONSERVATION_LAWS = {
    "energy": ("Time-translation symmetry (Noether)", "dE/dt = 0 in a closed system"),
    "momentum": ("Spatial-translation symmetry (Noether)", "sum p_i = const"),
    "angular_momentum": ("Rotational symmetry (Noether)", "sum L_i = const"),
    "charge": ("U(1) gauge symmetry", "total electric charge Q = const"),
    "probability": ("Unitarity of time evolution", "integral |psi|^2 d^3x = 1"),
    "baryon_number": ("U(1) baryon symmetry", "B = const (in SM, perturbatively)"),
    "lepton_number": ("U(1) lepton symmetries", "L_e, L_mu, L_tau approx conserved"),
}


FIELD_GRAPH = {
    "classical_mechanics": ["thermodynamics", "electrodynamics", "special_relativity", "general_relativity"],
    "electrodynamics": ["classical_mechanics", "special_relativity", "quantum_mechanics", "quantum_field_theory"],
    "quantum_mechanics": ["quantum_field_theory", "statistical_mechanics", "condensed_matter", "electrodynamics"],
    "thermodynamics": ["statistical_mechanics", "classical_mechanics", "condensed_matter"],
    "special_relativity": ["electrodynamics", "general_relativity", "particle_kinematics"],
    "general_relativity": ["special_relativity", "astrophysics_cosmology"],
    "quantum_field_theory": ["quantum_mechanics", "special_relativity", "statistical_mechanics"],
    "astrophysics_cosmology": ["general_relativity", "thermodynamics", "nuclear_physics"],
    "condensed_matter": ["quantum_mechanics", "statistical_mechanics", "electrodynamics"],
}


class KnowledgeEngine:
    """Lookup of conservation laws and the inter-domain field graph."""

    def conservation(self, quantity: str) -> tuple[str, str]:
        try:
            return CONSERVATION_LAWS[quantity.lower()]
        except KeyError as exc:
            raise KeyError(f"Unknown conserved quantity: {quantity}") from exc

    def related_fields(self, field: str) -> list[str]:
        return FIELD_GRAPH.get(field, [])

    def all_fields(self) -> list[str]:
        return list(FIELD_GRAPH.keys())

    def shortest_path(self, src: str, dst: str) -> list[str] | None:
        """BFS over the field graph connecting two domains."""
        from collections import deque
        if src == dst:
            return [src]
        seen = {src}
        q = deque([(src, [src])])
        while q:
            node, path = q.popleft()
            for nbr in FIELD_GRAPH.get(node, []):
                if nbr == dst:
                    return path + [nbr]
                if nbr not in seen:
                    seen.add(nbr)
                    q.append((nbr, path + [nbr]))
        return None


KNOWLEDGE = KnowledgeEngine()
