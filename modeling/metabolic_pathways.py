"""SBML diagrams and metabolic network graphs."""
from __future__ import annotations

from ai_core.knowledge_engine import KEGG_PATHWAYS


class MetabolicPathway:
    @staticmethod
    def build_graph(reactions: list[dict]) -> dict:
        nodes = set()
        edges = []
        for rxn in reactions:
            subs = rxn.get("substrates", [])
            prods = rxn.get("products", [])
            enzyme = rxn.get("enzyme", rxn.get("id", "rxn"))
            nodes.update(subs + prods + [enzyme])
            for s in subs:
                edges.append({"from": s, "to": enzyme, "type": "substrate"})
            for p in prods:
                edges.append({"from": enzyme, "to": p, "type": "product"})
        return {"nodes": sorted(nodes), "edges": edges, "n_reactions": len(reactions)}

    @staticmethod
    def pathway_lookup(kegg_id: str) -> str | None:
        return KEGG_PATHWAYS.get(kegg_id)

    @staticmethod
    def stoichiometric_matrix(reactions: list[dict]) -> dict:
        """Build S-matrix from reactions (metabolite x reaction)."""
        metabolites = sorted({m for r in reactions
                              for m in r.get("substrates", []) + r.get("products", [])})
        rxn_ids = [r.get("id", f"r{i}") for i, r in enumerate(reactions)]
        matrix = {m: [0.0] * len(reactions) for m in metabolites}
        for j, r in enumerate(reactions):
            for s in r.get("substrates", []):
                matrix[s][j] -= 1.0
            for p in r.get("products", []):
                matrix[p][j] += 1.0
        return {"metabolites": metabolites, "reactions": rxn_ids, "S": matrix}

    @staticmethod
    def to_sbml_lite(reactions: list[dict]) -> str:
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<sbml xmlns="http://www.sbml.org/sbml/level3/version1/core">']
        for i, r in enumerate(reactions):
            rid = r.get("id", f"r{i}")
            lines.append(f'  <reaction id="{rid}" reversible="false">')
            lines.append('    <listOfReactants>')
            for s in r.get("substrates", []):
                lines.append(f'      <speciesReference species="{s}"/>')
            lines.append('    </listOfReactants>')
            lines.append('    <listOfProducts>')
            for p in r.get("products", []):
                lines.append(f'      <speciesReference species="{p}"/>')
            lines.append('    </listOfProducts>')
            lines.append('  </reaction>')
        lines.append('</sbml>')
        return "\n".join(lines)
