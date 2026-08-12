"""Gibson assembly, Golden Gate, and ligation plans."""
from __future__ import annotations

from genetic_engineering.plasmid_builder import PlasmidBuilder


class CloningPlanner:
    def gibson_assembly(self, fragments: list[str], overlap: int = 20) -> dict:
        """Plan Gibson assembly with required homology overlaps."""
        if len(fragments) < 2:
            return {"error": "Need at least 2 fragments"}
        prepped = []
        for i, frag in enumerate(fragments):
            if i == 0:
                # add overlap to the 3' end matching next fragment's 5'
                ov = fragments[i + 1][:overlap] if i + 1 < len(fragments) else ""
                prepped.append(frag + ov)
            elif i == len(fragments) - 1:
                ov = fragments[i - 1][-overlap:]
                prepped.append(ov + frag)
            else:
                ov5 = fragments[i - 1][-overlap:]
                ov3 = fragments[i + 1][:overlap]
                prepped.append(ov5 + frag + ov3)
        total = sum(len(p) for p in prepped) - overlap * (len(prepped) - 1)
        return {
            "method": "Gibson assembly",
            "n_fragments": len(fragments),
            "overlap_bp": overlap,
            "prepped_fragments": prepped,
            "estimated_assembly_length": total,
            "enzymes": "T5 exonuclease, Phusion polymerase, Taq ligase",
            "temperature": "50 C, 60 min",
        }

    def golden_gate(self, parts: list[str], enzyme: str = "BsaI") -> dict:
        return {
            "method": "Golden Gate assembly",
            "enzyme": enzyme,
            "n_parts": len(parts),
            "overhang": "4 bp scarless",
            "note": "Type IIS enzyme cuts outside its recognition site enabling "
                    "scarless, multi-part assembly in one reaction",
        }

    def restriction_ligation(self, insert: str, vector: str,
                             enzyme: str = "EcoRI") -> dict:
        return PlasmidBuilder().build(insert, vector, enzyme)

    def recommend(self, insert: str, vector: str = "pUC19") -> str:
        pb = PlasmidBuilder()
        recs = pb.recommend_enzyme(insert)
        if recs:
            return f"For {vector}, use {recs[0]} (no internal sites in insert)."
        return "All common enzymes cut the insert; consider Gibson assembly."
