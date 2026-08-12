"""Check GMO and viral vector safety rules."""
from __future__ import annotations


class ContainmentChecker:
    @staticmethod
    def viral_vector_rules(vector: str) -> dict:
        v = vector.lower()
        rules = {}
        if "aav" in v:
            rules = {"risk_group": "RG1/RG2 (depending on transgene)",
                     "containment": "BSL-1/BSL-2",
                     "notes": "Replication-defective; check transgene hazard"}
        elif "lentivirus" in v:
            rules = {"risk_group": "RG2", "containment": "BSL-2",
                     "notes": "VSV-G pseudotyped; replication-incompetent required"}
        elif "adenovirus" in v:
            rules = {"risk_group": "RG2", "containment": "BSL-2",
                     "notes": "Replication-defective (E1/E3 deleted)"}
        elif "retrovirus" in v:
            rules = {"risk_group": "RG2", "containment": "BSL-2",
                     "notes": "Gamma-retroviral vectors require BSL-2"}
        else:
            rules = {"risk_group": "unknown",
                     "containment": "assess per institutional biosafety committee",
                     "notes": "Unknown vector type"}
        return {"vector": vector, **rules}

    @staticmethod
    def gmo_release_check(organism: str, trait: str = "") -> dict:
        org = organism.lower()
        if "escherichia coli" in org and "toxin" not in trait.lower():
            return {"permitted": True, "containment": "BSL-1 (K-12 derivatives)",
                    "cartagena_protocol": "subject to national GMO release regulations"}
        if "plant" in org:
            return {"permitted": False, "containment": "requires field trial permit",
                    "cartagena_protocol": "transboundary movement regulated"}
        return {"permitted": False, "containment": "case-by-case review required"}

    @staticmethod
    def institutional_biosafety_review(experiment: dict) -> str:
        if experiment.get("involves_pathogen") or experiment.get("involves_toxin"):
            return "IBC approval REQUIRED before initiation"
        if experiment.get("involves_viral_vector"):
            return "IBC registration required"
        return "Standard BSL-1 review sufficient"
