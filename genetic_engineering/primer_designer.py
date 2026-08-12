"""PCR primer design and Tm calculations."""
from __future__ import annotations

import re

from calculations.thermodynamic_calc import tm_gc_content, tm_wallace

PRIMER_RULES = {
    "min_length": 18,
    "max_length": 25,
    "min_gc": 40.0,
    "max_gc": 60.0,
    "min_tm": 55.0,
    "max_tm": 65.0,
    "max_self_complement": 4,
}


class PrimerDesigner:
    def design_primers(self, template: str, product_size: int = 500,
                       rules: dict | None = None) -> dict:
        rules = rules or PRIMER_RULES
        seq = re.sub(r"[^ACGT]", "", template.upper())
        if len(seq) < product_size or product_size < 2 * rules["min_length"]:
            return {"error": "Template too short for requested product size"}
        # forward primer: 5' end
        fwd = self._pick_primer(seq[:200], rules, forward=True)
        # reverse primer: 3' end reverse complement
        end_region = seq[-(product_size):]
        rev_candidates = []
        rc_full = _revcomp(seq)
        rev = self._pick_primer(rc_full[:200], rules, forward=True)
        return {
            "product_size": product_size,
            "forward_primer": fwd,
            "reverse_primer": rev,
            "tm_forward": round(tm_gc_content(fwd), 1) if fwd else None,
            "tm_reverse": round(tm_gc_content(rev), 1) if rev else None,
            "annealing_temp": round((tm_gc_content(fwd) + tm_gc_content(rev)) / 2 - 5, 1)
            if fwd and rev else None,
        }

    @staticmethod
    def _pick_primer(region, rules, forward=True):
        for length in range(rules["max_length"], rules["min_length"] - 1, -1):
            for start in range(0, len(region) - length + 1):
                cand = region[start:start + length]
                gc = _gc(cand)
                if not (rules["min_gc"] <= gc <= rules["max_gc"]):
                    continue
                tm = tm_gc_content(cand)
                if not (rules["min_tm"] <= tm <= rules["max_tm"]):
                    continue
                if _max_self_comp(cand) > rules["max_self_complement"]:
                    continue
                return cand
        return region[:rules["min_length"]]

    @staticmethod
    def melting_temp(seq, method="gc"):
        if method == "wallace":
            return tm_wallace(seq)
        return tm_gc_content(seq)

    @staticmethod
    def primer_efficiency_score(primer):
        gc = _gc(primer)
        tm = tm_gc_content(primer)
        score = 100.0
        score -= abs(gc - 50) * 0.5
        score -= abs(tm - 60) * 0.3
        if _max_self_comp(primer) > 4:
            score -= 10
        return round(max(score, 0), 1)


def _gc(seq):
    if not seq:
        return 0.0
    return 100.0 * (seq.count("G") + seq.count("C")) / len(seq)


def _revcomp(seq):
    return seq.translate(str.maketrans("ACGT", "TGCA"))[::-1]


def _max_self_comp(seq):
    """Crude self-complementarity estimate."""
    rc = _revcomp(seq)
    best = 0
    for i in range(len(seq)):
        run = 0
        for j in range(min(len(seq) - i, len(rc))):
            if seq[i + j] == rc[j]:
                run += 1
            else:
                best = max(best, run); run = 0
        best = max(best, run)
    return best
