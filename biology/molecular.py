"""DNA, RNA, and protein molecular biology."""
from __future__ import annotations

from biology._shared import extract_sequence, safe_ai_reason

_COMPLEMENT = str.maketrans("ACGTUNacgtun", "TGCAANtgcaan")
_CODON_TABLE = {
    # Standard genetic code (partial, all 64 codons)
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L",
    "CTT": "L", "CTC": "L", "CTA": "L", "CTG": "L",
    "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V",
    "TCT": "S", "TCC": "S", "TCA": "S", "TCG": "S",
    "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T",
    "GCT": "A", "GCC": "A", "GCA": "A", "GCG": "A",
    "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q",
    "AAT": "N", "AAC": "N", "AAA": "K", "AAG": "K",
    "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W",
    "CGT": "R", "CGC": "R", "CGA": "R", "CGG": "R",
    "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}


class MolecularModule:
    def handle(self, command: str, query: str, ctx) -> str:
        q = query.lower()
        if "transcrib" in q or "rna" in q:
            seq = extract_sequence(query)
            return f"Transcribed RNA (5'->3'): {self.transcribe(seq)}"
        if "translat" in q or "protein" in q:
            seq = extract_sequence(query)
            prot, stops = self.translate(seq)
            return f"Translated protein: {prot}\nStop codons: {stops}"
        if "complement" in q or "reverse" in q:
            seq = extract_sequence(query)
            return (
                f"Complement: {self.complement(seq)}\n"
                f"Reverse complement: {self.reverse_complement(seq)}"
            )
        if "gc" in q or "content" in q:
            seq = extract_sequence(query)
            return f"GC content: {self.gc_content(seq):.2f}%"
        return safe_ai_reason(query, ctx)

    @staticmethod
    def transcribe(dna: str) -> str:
        return dna.upper().replace("T", "U")

    @staticmethod
    def complement(dna: str) -> str:
        return dna.upper().translate(_COMPLEMENT)

    @staticmethod
    def reverse_complement(dna: str) -> str:
        return dna.upper().translate(_COMPLEMENT)[::-1]

    @staticmethod
    def gc_content(dna: str) -> float:
        if not dna:
            return 0.0
        gc = dna.upper().count("G") + dna.upper().count("C")
        return 100.0 * gc / len(dna)

    @staticmethod
    def translate(dna: str) -> tuple[str, int]:
        dna = dna.upper().replace("U", "T")
        prot = []
        stops = 0
        for i in range(0, len(dna) - 2, 3):
            codon = dna[i : i + 3]
            aa = _CODON_TABLE.get(codon, "X")
            if aa == "*":
                stops += 1
                prot.append("*")
            else:
                prot.append(aa)
        return "".join(prot), stops

    @staticmethod
    def molecular_weight_dna(dna: str, double_stranded: bool = False) -> float:
        """Average MW of dsDNA ~ 660 g/mol per bp; ssDNA ~ 330."""
        n = len(dna)
        if n == 0:
            return 0.0
        return n * (660.0 if double_stranded else 330.0)
