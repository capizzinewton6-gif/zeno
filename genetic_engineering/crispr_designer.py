"""Design gRNA, off-target analysis, and Cas enzymes."""
from __future__ import annotations

import re

from ai_core.safety_layer import SafetyLayer
from calculations.thermodynamic_calc import tm_gc_content

PAM_PATTERNS = {
    "SpCas9": "NGG",
    "SaCas9": "NNGRRT",
    "Cas12a": "TTTV",
    "CasX": "TTCN",
}

CAS_INFO = {
    "SpCas9": {"pam": "NGG", "cut": "blunt 3bp upstream of PAM", "size_kda": 160},
    "SaCas9": {"pam": "NNGRRT", "cut": "blunt", "size_kda": 120},
    "Cas12a": {"pam": "TTTV", "cut": "staggered, 18-23 nt 5' overhang", "size_kda": 130},
}


class CRISPRDesigner:
    def __init__(self):
        self.safety = SafetyLayer()

    def design_grna(self, target_sequence: str, pam: str = "NGG",
                    cas: str = "SpCas9", spacer_length: int = 20) -> dict:
        verdict = self.safety.screen_sequence(target_sequence)
        if not verdict:
            return {"error": verdict.reason}
        seq = re.sub(r"[^ACGT]", "", target_sequence.upper())
        # PAM orientation: Cas9 PAMs are 3' of the guide (spacer upstream);
        # Cas12a PAM is 5' of the guide (spacer downstream).
        pam_5prime = cas in ("Cas12a", "CasX")
        candidates = []
        for i in range(len(seq) - len(pam) + 1):
            window = seq[i:i + len(pam)]
            if not self._pam_match(window, pam):
                continue
            if pam_5prime:
                spacer = seq[i + len(pam): i + len(pam) + spacer_length]
                pos = i + len(pam)
                strand = "+"
            else:
                spacer = seq[i - spacer_length: i]
                pos = i - spacer_length
                strand = "+"
            if len(spacer) != spacer_length or pos < 0:
                continue
            candidates.append({
                "position": pos,
                "pam": window,
                "spacer": spacer,
                "strand": strand,
                "guide_rna": spacer + "guuuuagagcuagaaauagc".upper().replace("U", "T"),
                "gc_content": _gc(spacer),
                "estimated_tm": round(tm_gc_content(spacer), 1),
            })
        # reverse-strand candidates: search the reverse complement the same way
        rc = _revcomp(seq)
        for i in range(len(rc) - len(pam) + 1):
            window = rc[i:i + len(pam)]
            if not self._pam_match(window, pam):
                continue
            if pam_5prime:
                spacer = rc[i + len(pam): i + len(pam) + spacer_length]
                pos = i + len(pam)
            else:
                spacer = rc[i - spacer_length: i]
                pos = i - spacer_length
            if len(spacer) != spacer_length or pos < 0:
                continue
            candidates.append({
                "position": len(seq) - pos - spacer_length,
                "pam": window,
                "spacer": spacer,
                "strand": "-",
                "guide_rna": spacer + "guuuuagagcuagaaauagc".upper().replace("U", "T"),
                "gc_content": _gc(spacer),
                "estimated_tm": round(tm_gc_content(spacer), 1),
            })
        # filter for reasonable GC (30-70%) preferred guides
        for c in candidates:
            c["off_target_risk"] = self._off_target_risk(c["spacer"])
        ranked = sorted(candidates, key=lambda c: (c["off_target_risk"],
                                                   abs(c["gc_content"] - 50)))
        return {
            "cas": cas,
            "cas_info": CAS_INFO.get(cas, {}),
            "target_length": len(seq),
            "n_candidates": len(candidates),
            "top_guides": ranked[:5],
        }

    @staticmethod
    def _pam_match(window, pam):
        if len(window) != len(pam):
            return False
        for w, p in zip(window, pam):
            if p == "N":
                continue
            if p == "V" and w not in "ACG":
                return False
            if p == "R" and w not in "AG":
                return False
            if p == "T":
                if w != "T":
                    return False
            elif p != "N" and p != "V" and p != "R":
                if w != p:
                    return False
        return True

    @staticmethod
    def _off_target_risk(spacer):
        """Heuristic: lower GC extremes and poly-T runs raise off-target risk."""
        gc = _gc(spacer)
        risk = abs(gc - 50) / 50.0
        if "TTTT" in spacer:
            risk += 0.2
        return round(min(risk, 1.0), 3)


def _gc(seq):
    if not seq:
        return 0.0
    return 100.0 * (seq.count("G") + seq.count("C")) / len(seq)


def _revcomp(seq):
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]
