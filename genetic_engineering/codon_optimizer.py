"""Host-specific codon optimization for expression."""
from __future__ import annotations

from biology.molecular import MolecularModule

# Standard codon table -> amino acid
CODON_TABLE = {
    "TTT": "F", "TTC": "F", "TTA": "L", "TTG": "L", "CTT": "L", "CTC": "L",
    "CTA": "L", "CTG": "L", "ATT": "I", "ATC": "I", "ATA": "I", "ATG": "M",
    "GTT": "V", "GTC": "V", "GTA": "V", "GTG": "V", "TCT": "S", "TCC": "S",
    "TCA": "S", "TCG": "S", "CCT": "P", "CCC": "P", "CCA": "P", "CCG": "P",
    "ACT": "T", "ACC": "T", "ACA": "T", "ACG": "T", "GCT": "A", "GCC": "A",
    "GCA": "A", "GCG": "A", "TAT": "Y", "TAC": "Y", "TAA": "*", "TAG": "*",
    "CAT": "H", "CAC": "H", "CAA": "Q", "CAG": "Q", "AAT": "N", "AAC": "N",
    "AAA": "K", "AAG": "K", "GAT": "D", "GAC": "D", "GAA": "E", "GAG": "E",
    "TGT": "C", "TGC": "C", "TGA": "*", "TGG": "W", "CGT": "R", "CGC": "R",
    "CGA": "R", "CGG": "R", "AGT": "S", "AGC": "S", "AGA": "R", "AGG": "R",
    "GGT": "G", "GGC": "G", "GGA": "G", "GGG": "G",
}

# Preferred codons per host (representative single codon per amino acid)
HOST_PREFERRED = {
    "escherichia coli": {
        "F": "TTC", "L": "CTG", "I": "ATC", "M": "ATG", "V": "GTG",
        "S": "AGC", "P": "CCG", "T": "ACC", "A": "GCC", "Y": "TAC",
        "H": "CAC", "Q": "CAG", "N": "AAC", "K": "AAG", "D": "GAC",
        "E": "GAG", "C": "TGC", "W": "TGG", "R": "CGC", "G": "GGC",
    },
    "saccharomyces cerevisiae": {
        "F": "TTC", "L": "CTG", "I": "ATC", "M": "ATG", "V": "GTG",
        "S": "TCT", "P": "CCA", "T": "ACC", "A": "GCT", "Y": "TAC",
        "H": "CAC", "Q": "CAG", "N": "AAC", "K": "AAG", "D": "GAC",
        "E": "GAG", "C": "TGC", "W": "TGG", "R": "AGA", "G": "GGA",
    },
    "homo sapiens": {
        "F": "TTC", "L": "CTG", "I": "ATC", "M": "ATG", "V": "GTG",
        "S": "AGC", "P": "CCC", "T": "ACC", "A": "GCC", "Y": "TAC",
        "H": "CAC", "Q": "CAG", "N": "AAC", "K": "AAG", "D": "GAC",
        "E": "GAG", "C": "TGC", "W": "TGG", "R": "AGG", "G": "GGC",
    },
}


class CodonOptimizer:
    def optimize(self, protein_seq: str, host: str = "escherichia coli",
                 avoid_restriction_sites: list[str] | None = None) -> dict:
        host = host.lower()
        table = HOST_PREFERRED.get(host)
        if table is None:
            return {"error": f"No codon usage table for host '{host}'"}
        prot = protein_seq.upper()
        if not prot.startswith("M"):
            prot = "M" + prot  # ensure start codon
        dna = []
        for aa in prot:
            if aa == "*":
                dna.append("TAA")
            else:
                dna.append(table.get(aa, CODON_TABLE.get("ATG", "ATG")))
        optimized = "".join(dna)
        # verify
        translated, stops = MolecularModule.translate(optimized)
        return {
            "host": host,
            "input_protein": protein_seq.upper(),
            "optimized_dna": optimized,
            "length_bp": len(optimized),
            "gc_content": round(_gc(optimized), 1),
            "translated_check": translated,
            "translation_matches": translated.rstrip("*") == protein_seq.upper(),
        }


def _gc(seq):
    if not seq:
        return 0.0
    return 100.0 * (seq.count("G") + seq.count("C")) / len(seq)
