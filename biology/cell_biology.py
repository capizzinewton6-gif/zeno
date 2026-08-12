"""Organelles, signaling pathways, and the cell cycle."""
from __future__ import annotations

from biology._shared import safe_ai_reason

ORGANELLES = {
    "nucleus": "Stores genetic material; site of transcription and replication.",
    "mitochondrion": "ATP production via oxidative phosphorylation; has its own DNA.",
    "endoplasmic reticulum": "Protein folding (rough ER) and lipid synthesis (smooth ER).",
    "golgi apparatus": "Modifies, sorts, and packages proteins for secretion.",
    "lysosome": "Degradative organelle with acid hydrolases.",
    "chloroplast": "Photosynthesis in plant cells; contains thylakoids.",
    "ribosome": "Translates mRNA into protein.",
    "cell membrane": "Phospholipid bilayer regulating transport and signaling.",
    "cytoskeleton": "Structural support and intracellular transport.",
    "peroxisome": "Oxidative reactions; breaks down fatty acids.",
}

SIGNALING_PATHWAYS = {
    "mapk": "Ras->Raf->MEK->ERK cascade driving proliferation and differentiation.",
    "pi3k-akt": "PI3K generates PIP3; Akt promotes survival and growth.",
    "wnt": "Wnt binding inhibits the destruction complex, stabilizing beta-catenin.",
    "notch": "Direct cell-cell signaling via receptor-ligand interaction.",
    "jak-stat": "Cytokine receptors activate JAKs that phosphorylate STATs.",
    "camp": "GPCR->adenylyl cyclase->cAMP->PKA signaling.",
    "tgf-beta": "Receptor serine/threonine kinases phosphorylate SMADs.",
    "nf-kb": "IKK activation releases NF-kB for inflammatory gene expression.",
}


class CellBiologyModule:
    def handle(self, command: str, query: str, ctx) -> str:
        q = query.lower()
        for name, info in ORGANELLES.items():
            if name in q:
                return f"{name.capitalize()}: {info}"
        return safe_ai_reason(query, ctx)

    @staticmethod
    def analyze_pathway(pathway: str) -> dict:
        key = pathway.lower().replace("-", "_")
        desc = SIGNALING_PATHWAYS.get(key, SIGNALING_PATHWAYS.get(pathway.lower()))
        return {"pathway": pathway, "description": desc or "Pathway not in local database."}

    @staticmethod
    def cell_cycle_phase(marker_profile: dict) -> str:
        ki67 = marker_profile.get("ki67", marker_profile.get("Ki67", 0))
        brdu = marker_profile.get("brdu", marker_profile.get("BrdU", 0))
        phospho_h3 = marker_profile.get("phospho_h3",
                                        marker_profile.get("phosphoH3", 0))
        if phospho_h3 and phospho_h3 > 0.5:
            return "M (mitosis)"
        if brdu and brdu > 0.5:
            return "S (synthesis)"
        if ki67 and ki67 > 0.5:
            return "G1/G2 (interphase, proliferating)"
        return "G0 (quiescent)"
