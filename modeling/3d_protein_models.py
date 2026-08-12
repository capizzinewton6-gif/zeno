"""PDB structures, AlphaFold outputs, and active sites."""
from __future__ import annotations

from pathlib import Path


class ProteinModel3D:
    @staticmethod
    def parse_pdb(path: str | Path) -> dict:
        """Parse ATOM records and return residue summary (Biopython when available)."""
        try:
            from Bio.PDB import PDBParser
            parser = PDBParser(QUIET=True)
            struct = parser.get_structure("model", path)
            residues = []
            for model in struct:
                for chain in model:
                    for res in chain:
                        if res.id[0] == " ":
                            residues.append({
                                "chain": chain.id,
                                "residue": res.resname,
                                "number": res.id[1],
                            })
            return {
                "id": struct.id,
                "n_models": len(list(struct)),
                "n_residues": len(residues),
                "residues": residues[:100],
            }
        except Exception:
            return ProteinModel3D._basic_pdb_parse(path)

    @staticmethod
    def _basic_pdb_parse(path: str | Path) -> dict:
        residues = []
        seen = set()
        for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("ATOM") or line.startswith("HETATM"):
                resname = line[17:20].strip()
                chain = line[21].strip()
                resnum = int(line[22:26])
                key = (chain, resname, resnum)
                if key not in seen:
                    seen.add(key)
                    residues.append({"chain": chain, "residue": resname, "number": resnum})
        return {"id": Path(path).stem, "n_residues": len(residues), "residues": residues[:100]}

    @staticmethod
    def alphafold_confidence(plddt: list[float]) -> dict:
        if not plddt:
            return {"error": "No pLDDT scores"}
        avg = sum(plddt) / len(plddt)
        high = sum(1 for p in plddt if p >= 90)
        return {
            "mean_plddt": round(avg, 1),
            "high_confidence_residues": high,
            "total": len(plddt),
            "confidence": ("very high" if avg >= 90 else
                            "high" if avg >= 70 else
                            "low" if avg >= 50 else "very low"),
        }

    @staticmethod
    def predict_active_site(residues: list[dict], catalytic_motifs: list[str]) -> list[dict]:
        matches = []
        for r in residues:
            for motif in catalytic_motifs:
                if motif.upper() in r["residue"].upper():
                    matches.append(r)
                    break
        return matches
