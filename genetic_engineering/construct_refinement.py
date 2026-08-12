"""Verify open reading frames and promoter strength."""
from __future__ import annotations

import re

from biology.molecular import MolecularModule

STOP_CODONS = {"TAA", "TAG", "TGA"}
START_CODON = "ATG"

PROMOTER_ELEMENTS = {
    "-35": "TTGACA",
    "-10": "TATAAT",
}


class ConstructRefinement:
    def find_orfs(self, sequence: str, min_length_aa: int = 30) -> list[dict]:
        seq = re.sub(r"[^ACGT]", "", sequence.upper())
        orfs = []
        for frame in range(3):
            i = frame
            while i < len(seq) - 2:
                if seq[i:i + 3] == START_CODON:
                    # scan for stop
                    j = i
                    prot = []
                    while j < len(seq) - 2:
                        codon = seq[j:j + 3]
                        if codon in STOP_CODONS:
                            break
                        prot.append(codon)
                        j += 3
                    if len(prot) >= min_length_aa:
                        orfs.append({
                            "frame": frame,
                            "start": i,
                            "stop": j,
                            "length_nt": j - i,
                            "length_aa": len(prot),
                        })
                    i = j + 3
                else:
                    i += 3
        return orfs

    def promoter_strength_score(self, promoter_region: str) -> dict:
        seq = re.sub(r"[^ACGT]", "", promoter_region.upper())
        # crude sigma70 -35/-10 motif matching
        m35 = _best_match(seq, PROMOTER_ELEMENTS["-35"])
        m10 = _best_match(seq, PROMOTER_ELEMENTS["-10"])
        score = (m35 * 0.5 + m10 * 0.5)
        return {
            "m35_match": m35,
            "m10_match": m10,
            "consensus_score": round(score, 2),
            "relative_strength": ("strong" if score >= 0.7
                                   else "medium" if score >= 0.4 else "weak"),
        }

    def verify_construct(self, sequence: str) -> dict:
        orfs = self.find_orfs(sequence)
        prot, stops = MolecularModule.translate(sequence)
        return {
            "length": len(sequence),
            "orfs": orfs,
            "longest_orf_aa": max((o["length_aa"] for o in orfs), default=0),
            "stop_codons": stops,
            "gc_content": _gc(sequence),
        }


def _gc(seq):
    if not seq:
        return 0.0
    return round(100.0 * (seq.count("G") + seq.count("C")) / len(seq), 1)


def _best_match(seq, motif):
    if len(seq) < len(motif):
        return 0.0
    best = 0
    for i in range(len(seq) - len(motif) + 1):
        m = sum(a == b for a, b in zip(seq[i:i + len(motif)], motif))
        best = max(best, m)
    return round(best / len(motif), 2)
