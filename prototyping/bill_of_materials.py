"""Bill of materials — chemical inventory, CAS registry numbers, solvent BOM."""


class BillOfMaterials:
    """Build a chemical bill of materials with CAS numbers."""

    CAS_REGISTRY = {
        "water": "7732-18-5",
        "ethanol": "64-17-5",
        "methanol": "67-56-1",
        "acetone": "67-64-1",
        "dichloromethane": "75-09-2",
        "tetrahydrofuran": "109-99-9",
        "toluene": "108-88-3",
        "hexanes": "110-54-3",
        "ethyl acetate": "141-78-6",
        "acetonitrile": "75-05-8",
        "sulfuric acid": "7664-93-9",
        "sodium hydroxide": "1310-73-2",
        "hydrochloric acid": "7647-01-0",
        "sodium chloride": "7647-14-5",
        "magnesium sulfate": "7487-88-9",
        "sodium carbonate": "497-19-8",
        "palladium on carbon": "7440-05-3",
        "triethylamine": "121-44-8",
    }

    def build(self, items):
        """items: list of {name, quantity, unit}."""
        bom = []
        for it in items:
            name = it["name"].lower()
            entry = {
                "name": it["name"],
                "cas": self.CAS_REGISTRY.get(name, "—"),
                "quantity": it.get("quantity"),
                "unit": it.get("unit"),
            }
            bom.append(entry)
        return {"bill_of_materials": bom, "n_items": len(bom)}

    def lookup_cas(self, name):
        return self.CAS_REGISTRY.get(name.lower(), "—")

    def list_reagents(self):
        return list(self.CAS_REGISTRY.keys())
