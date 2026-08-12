"""Generate assay sheets and experiment logs."""
from __future__ import annotations

from datetime import datetime


class Documentation:
    @staticmethod
    def assay_sheet(title: str, reagents: list[dict], protocol: list[str],
                    readout: str = "absorbance", safety_notes: str = "") -> dict:
        return {
            "title": title,
            "type": "assay_sheet",
            "reagents": reagents,
            "protocol_steps": protocol,
            "readout": readout,
            "safety_notes": safety_notes,
            "generated_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def experiment_log(experiment_id: str, steps: list[dict],
                       results: dict | None = None, deviations: str = "") -> dict:
        return {
            "experiment_id": experiment_id,
            "type": "experiment_log",
            "steps": steps,
            "results": results or {},
            "deviations_from_protocol": deviations,
            "logged_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    def materials_and_methods(title: str, reagents: list[dict],
                              equipment: list[str], procedure: list[str]) -> str:
        lines = [f"## {title}", "",
                 "### Reagents", ""]
        for r in reagents:
            lines.append(f"- {r.get('name','')}: {r.get('amount','')} {r.get('unit','')}")
        lines += ["", "### Equipment", ""]
        for e in equipment:
            lines.append(f"- {e}")
        lines += ["", "### Procedure", ""]
        for i, step in enumerate(procedure, 1):
            lines.append(f"{i}. {step}")
        return "\n".join(lines)
