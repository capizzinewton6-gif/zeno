"""Material selector — select precursors, binders, and doping agents."""


class MaterialSelector:
    """Select materials based on application requirements."""

    PRECURSORS = {
        "TiO2": {"precursors": ["Ti(OiPr)4", "TiCl4"], "application": "photocatalysis, DSSC"},
        "ZnO": {"precursors": ["zinc acetate", "zinc nitrate"], "application": "transparent electronics"},
        "ZrO2": {"precursors": ["ZrOCl2", "zirconium isopropoxide"], "application": "catalyst support"},
        "Cu2O": {"precursors": ["Cu(OAc)2", "CuSO4 + reducing agent"], "application": "photocatalysis"},
        "graphene": {"precursors": ["graphite (Hummers)", "CH4 (CVD)"], "application": "conductivity, sensors"},
    }

    BINDERS = {
        "PVDF": {"solvent": "NMP", "use": "Li-ion electrodes"},
        "PTFE": {"solvent": "water (emulsion)", "use": "fuel cells, membranes"},
        "Nafion": {"solvent": "alcohol/water", "use": "proton exchange"},
        "carboxymethyl cellulose": {"solvent": "water", "use": "aqueous electrodes"},
    }

    DOPANTS = {
        "N-TiO2": {"dopant": "nitrogen", "effect": "visible-light absorption"},
        "S-doped graphene": {"dopant": "sulfur", "effect": "tuned bandgap, catalysis"},
        "B-doped diamond": {"dopant": "boron", "effect": "conductivity"},
        "P-doped Si": {"dopant": "phosphorus", "effect": "n-type semiconductor"},
    }

    def select_precursor(self, target):
        return self.PRECURSORS.get(target, {"error": f"No precursor data for {target}"})

    def select_binder(self, application):
        for name, info in self.BINDERS.items():
            if application.lower() in info["use"].lower():
                return {"binder": name, **info}
        return {"binder": "PVDF", **self.BINDERS["PVDF"], "note": "default recommendation"}

    def select_dopant(self, base):
        for name, info in self.DOPANTS.items():
            if base.lower() in name.lower():
                return {"dopant": name, **info}
        return {"error": f"No dopant data for {base}"}

    def list_all(self):
        return {"precursors": list(self.PRECURSORS), "binders": list(self.BINDERS), "dopants": list(self.DOPANTS)}
