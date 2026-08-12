"""Compatibility checker — chemical reactivity and hazardous mixture prevention."""


class CompatibilityChecker:
    """Flag incompatible chemical combinations."""

    INCOMPATIBLE = {
        ("acids", "bases"): "Violent neutralization; heat release.",
        ("oxidizers", "flammables"): "Fire/explosion risk.",
        ("oxidizers", "reducing agents"): "Violent redox reaction.",
        ("cyanides", "acids"): "Releases highly toxic HCN gas.",
        ("hypochlorite", "ammonia"): "Forms toxic chloramine gas.",
        ("hydrogen peroxide", "organics/metals"): "Decomposition / fire risk.",
        ("nitric acid", "organics"): "Violent oxidation; possible detonation.",
        ("sodium", "water"): "Violent reaction; hydrogen ignition.",
        ("permanganate", "glycerol"): "Spontaneous ignition.",
    }

    GROUPS = {
        "acids": ["sulfuric acid", "hydrochloric acid", "nitric acid", "acetic acid"],
        "bases": ["sodium hydroxide", "potassium hydroxide", "ammonia"],
        "oxidizers": ["hydrogen peroxide", "potassium permanganate", "nitric acid", "hypochlorite"],
        "flammables": ["ethanol", "acetone", "hexanes", "diethyl ether", "toluene"],
        "reducing agents": ["sodium borohydride", "lithium aluminum hydride", "sodium"],
        "cyanides": ["sodium cyanide", "potassium cyanide"],
        "water_reactive": ["sodium", "potassium", "lithium aluminum hydride", "calcium hydride"],
    }

    def _group_of(self, chemical):
        cl = chemical.lower()
        for group, members in self.GROUPS.items():
            for m in members:
                if m in cl or cl in m:
                    return group
        return None

    def check_pair(self, chem_a, chem_b):
        ga, gb = self._group_of(chem_a), self._group_of(chem_b)
        if not ga or not gb:
            return {"compatible": None, "note": "Group unknown; verify manually."}
        for (a, b), msg in self.INCOMPATIBLE.items():
            if (ga == a and gb == b) or (ga == b and gb == a):
                return {"compatible": False, "group_a": ga, "group_b": gb, "hazard": msg}
        return {"compatible": True, "group_a": ga, "group_b": gb, "note": "No known incompatibility."}

    def check_mixture(self, chemicals):
        warnings = []
        for i in range(len(chemicals)):
            for j in range(i + 1, len(chemicals)):
                result = self.check_pair(chemicals[i], chemicals[j])
                if result.get("compatible") is False:
                    warnings.append({"pair": [chemicals[i], chemicals[j]], **result})
        return {"mixture": chemicals, "warnings": warnings, "safe": len(warnings) == 0}
