"""Stereocontrol planner — asymmetric synthesis and enantiomeric resolution."""


class StereocontrolPlanner:
    """Asymmetric synthesis and resolution strategies."""

    STRATEGIES = {
        "chiral_auxiliary": {
            "description": "Attach a chiral auxiliary to control stereoselectivity.",
            "examples": ["Evans oxazolidinone", "Oppolzer sultam"],
        },
        "asymmetric_catalysis": {
            "description": "Use chiral catalyst for enantioselective transformation.",
            "examples": ["Noyori hydrogenation", "Sharpless epoxidation", "Corey-Bakshi-Shibata"],
        },
        "chiral_pool": {
            "description": "Start from enantiopure natural products.",
            "examples": ["amino acids", "terpenes", "sugars"],
        },
        "kinetic_resolution": {
            "description": "Selectively react one enantiomer.",
            "examples": ["enzymatic resolution", "Sharpless kinetic resolution"],
        },
        "chromatographic_resolution": {
            "description": "Separate enantiomers on chiral stationary phase.",
            "examples": ["chiral HPLC", "simulated moving bed"],
        },
    }

    def recommend(self, transformation=None, has_stereocenter=False):
        recs = []
        for key, info in self.STRATEGIES.items():
            recs.append({"strategy": key, "description": info["description"], "examples": info["examples"]})
        return {
            "transformation": transformation,
            "strategies": recs,
            "note": "Select strategy based on substrate, scale, and enantiopurity targets.",
        }

    @staticmethod
    def enantiomeric_excess(major, minor):
        total = major + minor
        if total == 0:
            return 0.0
        return (major - minor) / total * 100.0

    @staticmethod
    def optical_purity(ee_pct):
        return ee_pct / 100.0

    def list_strategies(self):
        return list(self.STRATEGIES.keys())
