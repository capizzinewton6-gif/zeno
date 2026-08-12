"""Classify Biosafety Levels (BSL-1 to BSL-4)."""
from __future__ import annotations


BSL_LEVELS = {
    "BSL-1": {
        "description": "Agents not known to cause disease in healthy adults",
        "examples": ["Bacillus subtilis", "E. coli K-12", "Saccharomyces cerevisiae"],
        "containment": "open bench, no special barriers",
        "ppe": "lab coat, gloves",
    },
    "BSL-2": {
        "description": "Agents causing moderate hazard via ingestion/skin/mucosal exposure",
        "examples": ["Staphylococcus aureus", "Salmonella", "Hepatitis B virus"],
        "containment": "BSC for aerosol-generating procedures, restricted access",
        "ppe": "lab coat, gloves, eye protection",
    },
    "BSL-3": {
        "description": "Agents causing serious/lethal disease via inhalation",
        "examples": ["Mycobacterium tuberculosis", "SARS-CoV-2", "Yersinia pestis"],
        "containment": "BSC, directional airflow, double-door autoclave",
        "ppe": "respiratory protection, dedicated lab clothing",
    },
    "BSL-4": {
        "description": "Dangerous agents with no treatment/vaccine, high lethality",
        "examples": ["Ebola virus", "Marburg virus", "Lassa fever virus"],
        "containment": "positive-pressure suit or Class III BSC, dedicated building systems",
        "ppe": "full positive-pressure suit",
    },
}


def _common_name(ex_l: str) -> str:
    """Map abbreviated scientific names to expanded common forms for matching."""
    return (ex_l
            .replace("e. coli", "escherichia coli")
            .replace("m. tuberculosis", "mycobacterium tuberculosis")
            .replace("s. aureus", "staphylococcus aureus"))


class BSLClassifier:
    @staticmethod
    def classify(organism: str) -> dict:
        org = organism.lower()
        for level, info in BSL_LEVELS.items():
            for ex in info["examples"]:
                ex_l = ex.lower()
                if org == ex_l or ex_l in org or _common_name(ex_l) in org:
                    return {"organism": organism, "bsl_level": level, **info}
        return {"organism": organism, "bsl_level": "unknown",
                "recommendation": "Refer to institutional biosafety committee for classification."}

    @staticmethod
    def all_levels() -> dict:
        return BSL_LEVELS

    @staticmethod
    def required_facilities(level: str) -> str:
        return BSL_LEVELS.get(level.upper(), {}).get("containment",
                                                      "Unknown level")
