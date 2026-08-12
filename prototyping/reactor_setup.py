"""Reactor setup — Schlenk line, autoclave, continuous flow, and reflux setups."""


class ReactorSetup:
    """Recommend reactor configurations."""

    SETUPS = {
        "schlenk_line": {
            "use": "air/moisture-sensitive chemistry",
            "components": ["dual manifold (vacuum/inert gas)", "Schlenk flask", "cold trap", "oil pump"],
            "checks": ["leak test", "inert gas purge cycles (x3)", "cold trap Dewar filled"],
        },
        "autoclave": {
            "use": "high-pressure hydrogenation / carbonylation",
            "components": ["pressure vessel", "gas inlet/regulator", "burst disk", "magnetic stirrer"],
            "checks": ["pressure test", "safety burst disk intact", "gas line purged"],
        },
        "continuous_flow": {
            "use": "scalable synthesis with precise residence control",
            "components": ["HPLC pumps", "mixer tee", "reactor coil/tube", "back-pressure regulator"],
            "checks": ["flow rate calibration", "tube volume measured", "BPR set"],
        },
        "reflux": {
            "use": "sustained heating at solvent boiling point",
            "components": ["round-bottom flask", "reflux condenser", "heating mantle", "stir bar"],
            "checks": ["cooling water flow", "boiling chips", "mantle temp set"],
        },
    }

    def recommend(self, setup_type):
        info = self.SETUPS.get(setup_type)
        if not info:
            return {"error": f"Unknown setup: {setup_type}", "available": list(self.SETUPS.keys())}
        return {"setup": setup_type, **info}

    def list_setups(self):
        return list(self.SETUPS.keys())
