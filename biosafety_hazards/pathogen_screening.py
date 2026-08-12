"""Screen sequences for toxins and regulated pathogens."""
from __future__ import annotations

from ai_core.safety_layer import SafetyLayer, SELECT_AGENTS, REGULATED_TOXINS

PATHOGEN_MARKERS = {
    "Bacillus anthracis": ["protective antigen", "lethal factor", "edema factor"],
    "Yersinia pestis": ["yersinia pestis", "plague"],
    "Variola virus": ["variola", "smallpox"],
    "Ebola virus": ["ebola", "filovirus"],
    "Francisella tularensis": ["tularemia", "francisella"],
}


class PathogenScreening:
    def __init__(self):
        self.safety = SafetyLayer()

    def screen_sequence(self, sequence: str, annotation: str = "") -> dict:
        verdict = self.safety.screen_sequence(sequence)
        return {
            "passed": bool(verdict),
            "reason": getattr(verdict, "reason", "") if not verdict else "no regulated markers detected",
            "screened_markers": list(REGULATED_TOXINS) + list(SELECT_AGENTS),
        }

    def screen_annotation(self, annotation: str) -> dict:
        ann = annotation.lower()
        hits = []
        for pathogen, markers in PATHOGEN_MARKERS.items():
            if pathogen.lower() in ann or any(m.lower() in ann for m in markers):
                hits.append(pathogen)
        return {
            "regulated_pathogen_detected": bool(hits),
            "matches": hits,
            "action": "halt and notify biosafety officer" if hits else "proceed",
        }

    @staticmethod
    def toxin_gene_check(gene_name: str) -> bool:
        return gene_name.lower() in {t.lower() for t in REGULATED_TOXINS}
