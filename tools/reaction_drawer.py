"""Reaction drawer — generate publication-quality reaction schemes and figures.

Generates SVG reaction schemes from SMILES/labels when RDKit is unavailable,
and richer depictions when RDKit is installed.
"""

import os
import html


class ReactionDrawer:
    """Render reaction schemes for the UI."""

    def __init__(self, output_dir="static/reactions"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self._rdkit = None
        try:
            from rdkit import Chem
            from rdkit.Chem import Draw
            self._rdkit = {"Chem": Chem, "Draw": Draw}
        except Exception:
            self._rdkit = None

    def draw_scheme(self, reactants, products, conditions="", title="Reaction Scheme"):
        """reactants/products: list of SMILES or label strings."""
        if self._rdkit:
            try:
                Chem = self._rdkit["Chem"]
                Draw = self._rdkit["Draw"]
                r_mols = [Chem.MolFromSmiles(s) or Chem.MolFromSmiles(self._label_smiles(s)) for s in reactants]
                p_mols = [Chem.MolFromSmiles(s) or Chem.MolFromSmiles(self._label_smiles(s)) for s in products]
                r_mols = [m for m in r_mols if m is not None]
                p_mols = [m for m in p_mols if m is not None]
                if r_mols and p_mols:
                    img = Draw.ReactionToImage(((r_mols, p_mols),))
                    path = os.path.join(self.output_dir, "reaction_rdkit.png")
                    img.save(path)
                    return {"image": path, "engine": "rdkit"}
            except Exception:
                pass
        return self._svg_scheme(reactants, products, conditions, title)

    def _label_smiles(self, label):
        """Map common labels to placeholder SMILES."""
        mapping = {"water": "O", "ethanol": "CCO", "methanol": "CO",
                   "acetone": "CC(=O)C", "HCl": "Cl", "NaOH": "[Na+].[OH-]"}
        return mapping.get(str(label).lower(), "C")

    def _svg_scheme(self, reactants, products, conditions, title):
        r_text = " + ".join(html.escape(str(r)) for r in reactants)
        p_text = " + ".join(html.escape(str(p)) for p in products)
        cond = html.escape(conditions)
        svg = f"""<svg xmlns='http://www.w3.org/2000/svg' width='640' height='160' viewBox='0 0 640 160'>
  <rect width='640' height='160' fill='#0d1117' rx='8'/>
  <text x='320' y='24' font-family='sans-serif' font-size='14' fill='#8b949e' text-anchor='middle'>{html.escape(title)}</text>
  <text x='160' y='85' font-family='monospace' font-size='13' fill='#58a6ff' text-anchor='middle'>{r_text}</text>
  <line x1='300' y1='80' x2='360' y2='80' stroke='#c9d1d9' stroke-width='2'/>
  <polygon points='360,80 352,76 352,84' fill='#c9d1d9'/>
  <text x='330' y='68' font-family='sans-serif' font-size='10' fill='#7ee787' text-anchor='middle'>{cond}</text>
  <text x='500' y='85' font-family='monospace' font-size='13' fill='#ff7b72' text-anchor='middle'>{p_text}</text>
</svg>"""
        path = os.path.join(self.output_dir, "reaction_scheme.svg")
        with open(path, "w") as f:
            f.write(svg)
        return {"image": path, "engine": "svg", "svg": svg}
