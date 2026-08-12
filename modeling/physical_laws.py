"""Fundamental principles: conservation of energy, charge, entropy."""

from __future__ import annotations

from ai_core.knowledge_engine import CONSERVATION_LAWS


PRINCIPLES = {
    "energy_conservation": "In a closed, time-translation-invariant system, total energy is conserved.",
    "momentum_conservation": "Spatial-translation invariance implies total momentum conservation.",
    "angular_momentum_conservation": "Rotational invariance implies total angular momentum conservation.",
    "charge_conservation": "U(1) gauge invariance implies total electric charge conservation.",
    "entropy": "Second law: the total entropy of an isolated system never decreases.",
    "causality": "No signal propagates faster than light; cause precedes effect within light cones.",
    "unitarity": "Quantum time evolution preserves total probability: |S|^2 summed = 1.",
    "equivalence_principle": "Local effects of gravity and acceleration are indistinguishable.",
    "least_action": "The physical path extremizes the action S = integral L dt.",
}


class PhysicalLaws:
    """Enumerate fundamental principles and their conservation-law mappings."""

    @staticmethod
    def principle(name: str) -> str:
        try:
            return PRINCIPLES[name.lower()]
        except KeyError as exc:
            raise KeyError(f"Unknown principle: {name}") from exc

    @staticmethod
    def all_principles() -> dict[str, str]:
        return dict(PRINCIPLES)

    @staticmethod
    def conservation_laws() -> dict[str, tuple[str, str]]:
        return dict(CONSERVATION_LAWS)
