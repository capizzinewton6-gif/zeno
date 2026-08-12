"""Autoclaving, biohazard waste, and decontamination."""
from __future__ import annotations


class WasteDisposal:
    AUTOCLAVE_PARAMS = {
        "standard": {"temp_c": 121, "time_min": 15, "pressure_psi": 15},
        "liquid": {"temp_c": 121, "time_min": 30, "pressure_psi": 15},
        "prion_waste": {"temp_c": 134, "time_min": 60, "pressure_psi": 30},
    }

    DISINFECTANTS = {
        "70% ethanol": {"spectrum": "vegetative bacteria, fungi, enveloped viruses",
                        "contact_min": 1, "notes": "not sporicidal"},
        "10% bleach": {"spectrum": "broad, including some spores",
                       "contact_min": 10, "notes": "corrosive to metal"},
        "quaternary ammonium": {"spectrum": "vegetative bacteria, viruses",
                                "contact_min": 5, "notes": "limited vs. spores"},
        "glutaraldehyde": {"spectrum": "broad incl. spores, mycobacteria",
                           "contact_min": 20, "notes": "toxic; ventilate"},
        "UV-C": {"spectrum": "surface DNA/RNA damage",
                 "contact_min": 15, "notes": "line-of-sight only"},
    }

    @staticmethod
    def autoclave_cycle(waste_type: str = "standard") -> dict:
        params = WasteDisposal.AUTOCLAVE_PARAMS.get(waste_type,
                                                     WasteDisposal.AUTOCLAVE_PARAMS["standard"])
        return {"waste_type": waste_type, "cycle": params,
                "sterility_assurance_level": "10^-6 (SAL6)",
                "indicator": "biological (Geobacillus stearothermophilus)"}

    @staticmethod
    def recommend_disinfectant(target: str) -> list[str]:
        t = target.lower()
        if "spore" in t:
            return ["10% bleach", "glutaraldehyde"]
        if "virus" in t or "enveloped" in t:
            return ["70% ethanol", "10% bleach", "quaternary ammonium"]
        if "bacteria" in t:
            return ["70% ethanol", "10% bleach"]
        return ["10% bleach"]

    @staticmethod
    def waste_classification(waste: str) -> dict:
        w = waste.lower()
        if "sharps" in w or "needle" in w:
            return {"category": "sharps waste", "disposal": "puncture-resistant container, autoclave, incinerate"}
        if "liquid" in w or "culture" in w:
            return {"category": "liquid biohazard", "disposal": "autoclave (liquid cycle), then drain"}
        if "solid" in w or "plate" in w or "tip" in w:
            return {"category": "solid biohazard", "disposal": "autoclave bag, autoclave, then landfill"}
        if "pathological" in w or "tissue" in w:
            return {"category": "pathological waste", "disposal": "incineration (regulated medical waste)"}
        return {"category": "general biohazard", "disposal": "autoclave then dispose per local regulations"}
