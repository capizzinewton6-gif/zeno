"""Reagent inventory, enzymes, and media BOM."""
from __future__ import annotations


class BillOfMaterials:
    def __init__(self):
        self.items: list[dict] = []

    def add(self, name: str, quantity: float, unit: str, catalog: str = "",
            unit_cost: float = 0.0) -> None:
        self.items.append({"name": name, "quantity": quantity, "unit": unit,
                           "catalog": catalog, "unit_cost": unit_cost,
                           "subtotal": round(quantity * unit_cost, 2)})

    def total(self) -> float:
        return round(sum(i["subtotal"] for i in self.items), 2)

    def summary(self) -> dict:
        return {"n_items": len(self.items), "total_cost": self.total(),
                "items": self.items}

    @staticmethod
    def pcr_bom(reactions: int, vol_per_reaction_ul: float = 25) -> "BillOfMaterials":
        bom = BillOfMaterials()
        total_vol = reactions * vol_per_reaction_ul
        bom.add("Taq polymerase", total_vol * 0.025, "U", unit_cost=0.1)
        bom.add("dNTP mix", total_vol * 0.2, "nmol", unit_cost=0.01)
        bom.add("Forward primer", total_vol * 0.5, "pmol", unit_cost=0.05)
        bom.add("Reverse primer", total_vol * 0.5, "pmol", unit_cost=0.05)
        bom.add("PCR buffer (10x)", total_vol * 0.1, "uL", unit_cost=0.001)
        bom.add("Template DNA", reactions, "uL", unit_cost=0.0)
        return bom
