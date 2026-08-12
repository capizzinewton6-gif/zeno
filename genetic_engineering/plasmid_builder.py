"""Vector construction and restriction site mapping."""
from __future__ import annotations

import re

COMMON_RESTRICTION_ENZYMES = {
    "EcoRI": ("GAATTC", 1),
    "BamHI": ("GGATCC", 1),
    "HindIII": ("AAGCTT", 1),
    "XhoI": ("CTCGAG", 1),
    "NotI": ("GCGGCCGC", 2),
    "NdeI": ("CATATG", 2),
    "XbaI": ("TCTAGA", 1),
    "KpnI": ("GGTACC", 1),
    "SacI": ("GAGCTC", 1),
    "BglII": ("AGATCT", 1),
}

VECTOR_DB = {
    "pUC19": {"size_bp": 2686, "copy_number": "high", "selection": "ampicillin",
              "mcs": "EcoRI, BamHI, HindIII, XbaI, KpnI"},
    "pBR322": {"size_bp": 4361, "copy_number": "medium", "selection": "ampicillin/tetracycline",
               "mcs": "EcoRI, BamHI, HindIII"},
    "pET28a": {"size_bp": 5369, "copy_number": "medium", "selection": "kanamycin",
               "mcs": "NdeI, XhoI, BamHI"},
    "pcDNA3.1": {"size_bp": 5428, "copy_number": "high", "selection": "ampicillin",
                 "mcs": "HindIII, XhoI, NotI, BamHI"},
}


class PlasmidBuilder:
    def map_sites(self, sequence: str) -> dict:
        seq = re.sub(r"[^ACGT]", "", sequence.upper())
        sites = {}
        for enzyme, (site, _) in COMMON_RESTRICTION_ENZYMES.items():
            positions = [m.start() for m in re.finditer(site, seq)]
            rc_site = site.translate(str.maketrans("ACGT", "TGCA"))[::-1]
            positions += [m.start() for m in re.finditer(rc_site, seq)]
            if positions:
                sites[enzyme] = sorted(set(positions))
        return {"length": len(seq), "sites": sites}

    def build(self, insert: str, vector: str = "pUC19",
              enzyme: str = "BamHI") -> dict:
        vec = VECTOR_DB.get(vector)
        if not vec:
            return {"error": f"Unknown vector {vector}"}
        insert_clean = re.sub(r"[^ACGT]", "", insert.upper())
        site, _ = COMMON_RESTRICTION_ENZYMES.get(enzyme, ("", 0))
        if not site:
            return {"error": f"Unknown enzyme {enzyme}"}
        total = vec["size_bp"] + len(insert_clean)
        return {
            "vector": vector,
            "vector_info": vec,
            "insert_length": len(insert_clean),
            "construct_size_bp": total,
            "cloning_enzyme": enzyme,
            "site": site,
            "selection": vec["selection"],
            "map": self.map_sites(insert_clean),
        }

    def recommend_enzyme(self, insert: str) -> list[str]:
        sites = self.map_sites(insert)["sites"]
        internal = set(sites.keys())
        return [e for e in COMMON_RESTRICTION_ENZYMES if e not in internal]
