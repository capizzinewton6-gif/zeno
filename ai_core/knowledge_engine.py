"""Gene Ontology and biological knowledge graph (lightweight local representation)."""
from __future__ import annotations

# Minimal built-in Gene Ontology / pathway lookup tables so the knowledge
# engine is useful offline. Real deployments would query an OBO/KG endpoint.
GO_TERMS = {
    "GO:0008150": ("biological_process", "A biological process."),
    "GO:0003674": ("molecular_function", "A molecular function."),
    "GO:0005575": ("cellular_component", "A cellular component."),
    "GO:0006355": ("biological_process", "Regulation of DNA-templated transcription."),
    "GO:0006412": ("biological_process", "Translation."),
    "GO:0007165": ("biological_process", "Signal transduction."),
    "GO:0005524": ("molecular_function", "ATP binding."),
    "GO:0005623": ("cellular_component", "Cell."),
    "GO:0005829": ("cellular_component", "Cytosol."),
    "GO:0005739": ("cellular_component", "Mitochondrion."),
}

KEGG_PATHWAYS = {
    "hsa00010": "Glycolysis / Gluconeogenesis",
    "hsa00020": "TCA cycle",
    "hsa00190": "Oxidative phosphorylation",
    "hsa03010": "Ribosome",
    "hsa04110": "Cell cycle",
    "hsa04115": "p53 signaling pathway",
    "hsa04151": "PI3K-Akt signaling pathway",
    "eco00010": "Glycolysis (E. coli)",
    "eco02010": "ABC transporters (E. coli)",
}

CENTRAL_DOGMA = ["DNA", "RNA", "Protein"]


class KnowledgeEngine:
    """Local biological knowledge graph lookup."""

    def lookup_go(self, go_id: str) -> dict | None:
        entry = GO_TERMS.get(go_id)
        if not entry:
            return None
        namespace, definition = entry
        return {"id": go_id, "namespace": namespace, "definition": definition}

    def search_go(self, keyword: str) -> list[dict]:
        kw = keyword.lower()
        return [
            {"id": gid, "namespace": ns, "definition": defn}
            for gid, (ns, defn) in GO_TERMS.items()
            if kw in defn.lower() or kw in ns.lower()
        ]

    def lookup_pathway(self, kegg_id: str) -> str | None:
        return KEGG_PATHWAYS.get(kegg_id)

    def search_pathways(self, keyword: str) -> list[dict]:
        kw = keyword.lower()
        return [{"id": k, "name": v} for k, v in KEGG_PATHWAYS.items() if kw in v.lower()]

    @staticmethod
    def central_dogma() -> list[str]:
        return list(CENTRAL_DOGMA)
