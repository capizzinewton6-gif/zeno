"""Genetic circuit design and BioBrick assembly."""
from __future__ import annotations

# BioBrick prefix/suffix standard (RFC 10)
BIOBRICK_PREFIX = "GAATTCGCGGCCGCTTCTAGA"   # EcoRI, NotI, XbaI
BIOBRICK_SUFFIX = "TACTAGTAGCGGCCGCTGCAG"    # SpeI, NotI, PstI


class SyntheticBiology:
    def design_circuit(self, promoter: str, rbs: str, cds: str,
                       terminator: str = "rrnB T1") -> dict:
        return {
            "promoter": promoter,
            "rbs": rbs,
            "cds": cds,
            "terminator": terminator,
            "circuit_topology": f"{promoter} -> {rbs} -> {cds} -> {terminator}",
            "expected_output": "constitutive or regulated expression of the CDS",
        }

    def biobrick_assemble(self, part1: str, part2: str) -> dict:
        composite = (
            BIOBRICK_PREFIX
            + part1.upper()
            + "TACTAGT"
            + part2.upper()
            + BIOBRICK_SUFFIX
        )
        return {
            "method": "BioBrick RFC 10 assembly",
            "scar_sequence": "TACTAGAG",
            "composite_part": composite,
            "length_bp": len(composite),
        }

    def logic_gate(self, gate_type: str, inputs: list[str]) -> dict:
        gates = {
            "AND": "both input promoters must be active to drive output",
            "OR": "either input promoter drives output",
            "NOT": "input represses output",
            "NAND": "both inputs repress output when active",
            "XOR": "output active when exactly one input active",
        }
        return {"gate": gate_type, "inputs": inputs,
                "behavior": gates.get(gate_type, "unknown gate")}
