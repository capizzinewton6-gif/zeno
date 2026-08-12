"""Central dogma, base pairing, and translation rules."""
from __future__ import annotations

from biology.molecular import MolecularModule

BASE_PAIRING = {"A": "T", "T": "A", "G": "C", "C": "G", "A": "U", "U": "A"}


class BiologicalRules:
    @staticmethod
    def complement(base: str) -> str:
        if len(base) != 1:
            raise ValueError("Provide a single base")
        return BASE_PAIRING.get(base.upper(), "?")

    @staticmethod
    def reverse_complement(seq: str) -> str:
        return MolecularModule.reverse_complement(seq)

    @staticmethod
    def transcribe(dna: str) -> str:
        return MolecularModule.transcribe(dna)

    @staticmethod
    def translate(rna: str) -> str:
        dna = rna.upper().replace("U", "T")
        prot, _ = MolecularModule.translate(dna)
        return prot

    @staticmethod
    def central_dogma(steps: list[str]) -> bool:
        """Validate a proposed central-dogma path."""
        allowed = {"replication", "transcription", "translation",
                   "reverse_transcription", "rna_replication"}
        return all(s in allowed for s in steps)

    @staticmethod
    def is_valid_dna(seq: str) -> bool:
        return set(seq.upper()) <= set("ACGT")

    @staticmethod
    def is_valid_protein(seq: str) -> bool:
        return set(seq.upper()) <= set("ACDEFGHIKLMNPQRSTVWY*")
