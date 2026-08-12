"""Cheminformatics — RDKit/OpenBabel SMILES parsing, substructure matching, fingerprinting.

Falls back to a lightweight pure-Python SMILES parser when RDKit is not
installed so the UI simulations remain functional.
"""

import hashlib
import re


class Cheminformatics:
    """SMILES parsing and molecular property helpers."""

    def __init__(self):
        self._rdkit = None
        try:
            from rdkit import Chem
            from rdkit.Chem import AllChem, Descriptors
            self._rdkit = {"Chem": Chem, "AllChem": AllChem, "Descriptors": Descriptors}
        except Exception:
            self._rdkit = None

    # --- SMILES parsing ------------------------------------------------
    def parse_smiles(self, smiles):
        if self._rdkit:
            mol = self._rdkit["Chem"].MolFromSmiles(smiles)
            if mol is None:
                return {"valid": False, "error": "Invalid SMILES (RDKit)"}
            return {
                "valid": True,
                "engine": "rdkit",
                "canonical_smiles": self._rdkit["Chem"].MolToSmiles(mol),
                "num_atoms": mol.GetNumAtoms(),
                "num_heavy_atoms": mol.GetNumHeavyAtoms(),
                "molecular_weight": round(self._rdkit["Descriptors"].MolWt(mol), 3),
                "num_rings": self._rdkit["Chem"].GetSymmSSSR(mol).GetNumRings(),
            }
        return self._fallback_parse(smiles)

    def _fallback_parse(self, smiles):
        """Very lightweight SMILES validator/count of organic atoms."""
        if not smiles:
            return {"valid": False, "error": "Empty SMILES"}
        organic = set("BCNOPSFI")
        counts = {}
        ring_digits = []
        i = 0
        valid = True
        while i < len(smiles):
            ch = smiles[i]
            if ch == "[":
                end = smiles.find("]", i)
                if end == -1:
                    valid = False
                    break
                token = smiles[i + 1:end]
                elem = re.match(r"([A-Za-z]+)", token)
                if elem:
                    counts[elem.group(1).capitalize()] = counts.get(elem.group(1).capitalize(), 0) + 1
                i = end + 1
            elif ch.isupper():
                elem = ch
                if i + 1 < len(smiles) and smiles[i + 1].islower():
                    elem += smiles[i + 1]
                    i += 1
                counts[elem] = counts.get(elem, 0) + 1
                i += 1
            elif ch.isdigit():
                ring_digits.append(ch)
                i += 1
            elif ch in "()-=#/\\.":
                i += 1
            else:
                valid = False
                i += 1
        ring_pairs = len(ring_digits) // 2
        return {
            "valid": valid,
            "engine": "fallback",
            "atom_counts": counts,
            "ring_closures_detected": ring_pairs,
            "note": "RDKit not available; using lightweight SMILES parser.",
        }

    # --- Substructure matching ----------------------------------------
    def substructure_match(self, mol_smiles, query_smarts):
        if self._rdkit:
            mol = self._rdkit["Chem"].MolFromSmiles(mol_smiles)
            patt = self._rdkit["Chem"].MolFromSmarts(query_smarts)
            if mol is None or patt is None:
                return {"match": False, "error": "Invalid input"}
            matches = mol.GetSubstructMatches(patt)
            return {"match": len(matches) > 0, "num_matches": len(matches), "matches": matches}
        return {"match": None, "error": "RDKit required for substructure matching."}

    # --- Fingerprints --------------------------------------------------
    def morgan_fingerprint(self, smiles, radius=2, n_bits=2048):
        if self._rdkit:
            mol = self._rdkit["Chem"].MolFromSmiles(smiles)
            if mol is None:
                return {"valid": False}
            from rdkit.Chem import rdFingerprintGenerator
            gen = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
            fp = gen.GetFingerprint(mol)
            return {"valid": True, "bits": list(fp.GetOnBits()), "n_bits": n_bits}
        # Deterministic hash-based pseudo-fingerprint fallback
        h = hashlib.md5(smiles.encode()).hexdigest()
        bits = [int(h[i:i+2], 16) % n_bits for i in range(0, len(h), 2)]
        return {"valid": True, "engine": "hash-fallback", "bits": sorted(set(bits)), "n_bits": n_bits}
