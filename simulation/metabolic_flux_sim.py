"""Flux Balance Analysis (FBA) for metabolic networks (linear programming)."""
from __future__ import annotations

from scipy.optimize import linprog


class FBASimulator:
    def run(self, reactions: list[dict], objective: str, maximize: bool = True) -> dict:
        """Simple FBA. reactions: list with 'id', 'substrates', 'products', 'bounds'."""
        S = self._stoichiometry(reactions)
        metabolites = sorted(S.keys())
        n_rxn = len(reactions)
        # objective vector: maximize obj -> minimize -obj
        c = [0.0] * n_rxn
        if objective in [r["id"] for r in reactions]:
            c[[r["id"] for r in reactions].index(objective)] = -1.0 if maximize else 1.0
        # S @ v = 0
        A_eq = [[S[m].get(r["id"], 0.0) for r in reactions] for m in metabolites]
        b_eq = [0.0] * len(metabolites)
        # bounds
        bounds = [tuple(r.get("bounds", (0, 1000))) for r in reactions]
        res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")
        if not res.success:
            return {"status": "infeasible", "message": res.message}
        fluxes = {r["id"]: round(res.x[i], 4) for i, r in enumerate(reactions)}
        objective_value = fluxes.get(objective, 0.0)
        return {"status": "optimal", "objective": objective, "objective_value": objective_value,
                "fluxes": fluxes}

    @staticmethod
    def _stoichiometry(reactions):
        S = {}
        for r in reactions:
            external = set(r.get("external", []))
            for s in r.get("substrates", []):
                if s in external:
                    continue
                S.setdefault(s, {})[r["id"]] = S.get(s, {}).get(r["id"], 0) - 1.0
            for p in r.get("products", []):
                if p in external:
                    continue
                S.setdefault(p, {})[r["id"]] = S.get(p, {}).get(r["id"], 0) + 1.0
        return S

    @staticmethod
    def optimize_media(organism: str, target: str = "biomass") -> dict:
        # heuristic recommendation rather than full reconstruction
        media = {
            "escherichia coli": ["glucose", "NH4", "phosphate", "O2"],
            "saccharomyces cerevisiae": ["glucose", "NH4", "phosphate", "O2"],
            "homo sapiens": ["glucose", "glutamine", "amino acids", "O2"],
        }
        recs = media.get(organism.lower(), ["carbon source", "N source", "P source"])
        return {"organism": organism, "target": target,
                "recommended_media": recs,
                "note": "Full FBA requires an organism-specific metabolic reconstruction."}
