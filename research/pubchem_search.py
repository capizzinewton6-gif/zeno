"""PubChem search — query PubChem, ChemSpider, and CAS Registry.

Uses the public PubChem PUG REST API. Network calls are wrapped so the UI
works offline (returns a structured note) when no connectivity is available.
"""

import json
import logging
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

PUBCHEM_REST = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"


class PubChemSearch:
    """Query PubChem for compound properties."""

    def by_name(self, name, properties=None):
        properties = properties or ["MolecularFormula", "MolecularWeight", "CanonicalSMILES", "IUPACName"]
        prop_str = ",".join(properties)
        url = f"{PUBCHEM_REST}/compound/name/{urllib.parse.quote(name)}/property/{prop_str}/JSON"
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.loads(r.read().decode())
            props = data.get("PropertyTable", {}).get("Properties", [])
            return {"source": "PubChem", "query": name, "results": props, "mode": "live"}
        except Exception as exc:
            logger.warning("PubChem query failed: %s", exc)
            return {"source": "PubChem", "query": name, "results": [],
                    "mode": "offline", "error": str(exc),
                    "note": "PubChem unreachable; provide network access for live queries."}

    def by_smiles(self, smiles, properties=None):
        properties = properties or ["MolecularFormula", "MolecularWeight"]
        prop_str = ",".join(properties)
        url = f"{PUBCHEM_REST}/compound/smiles/{urllib.parse.quote(smiles)}/property/{prop_str}/JSON"
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.loads(r.read().decode())
            props = data.get("PropertyTable", {}).get("Properties", [])
            return {"source": "PubChem", "query_smiles": smiles, "results": props, "mode": "live"}
        except Exception as exc:
            logger.warning("PubChem SMILES query failed: %s", exc)
            return {"source": "PubChem", "query_smiles": smiles, "results": [],
                    "mode": "offline", "error": str(exc)}

    def cas_like_lookup(self, name):
        """PubChem does not directly expose CAS, but synonyms often include it."""
        url = f"{PUBCHEM_REST}/compound/name/{urllib.parse.quote(name)}/synonyms/JSON"
        try:
            with urllib.request.urlopen(url, timeout=10) as r:
                data = json.loads(r.read().decode())
            info = data.get("InformationList", {}).get("Information", [])
            synonyms = info[0].get("Synonym", []) if info else []
            cas = [s for s in synonyms if s.count("-") == 2 and s.split("-")[-1].isdigit()]
            return {"source": "PubChem", "query": name, "cas_candidates": cas[:5], "mode": "live"}
        except Exception as exc:
            return {"source": "PubChem", "query": name, "cas_candidates": [],
                    "mode": "offline", "error": str(exc)}
