"""GHS classifier — GHS hazard classes, pictograms, and signal words."""

GHS_PICTOGRAMS = {
    "GHS01": "explosive",
    "GHS02": "flammable",
    "GHS03": "oxidizing",
    "GHS04": "gas under pressure",
    "GHS05": "corrosive",
    "GHS06": "toxic",
    "GHS07": "harmful/irritant",
    "GHS08": "health hazard",
    "GHS09": "environmental hazard",
}


class GHSClassifier:
    """Classify chemicals into GHS hazard categories."""

    HAZARD_DATA = {
        "hydrofluoric acid": {"pictograms": ["GHS05", "GHS06", "GHS08"], "signal_word": "Danger",
                              "h_statements": ["H300", "H310", "H314", "H330", "H361", "H372"]},
        "sodium hydroxide": {"pictograms": ["GHS05"], "signal_word": "Danger", "h_statements": ["H314", "H290"]},
        "ethanol": {"pictograms": ["GHS02", "GHS07"], "signal_word": "Danger", "h_statements": ["H225", "H319"]},
        "acetone": {"pictograms": ["GHS02", "GHS07"], "signal_word": "Danger", "h_statements": ["H225", "H319", "H336"]},
        "dichloromethane": {"pictograms": ["GHS07", "GHS08"], "signal_word": "Warning", "h_statements": ["H315", "H319", "H335", "H351", "H373"]},
        "toluene": {"pictograms": ["GHS02", "GHS07", "GHS08"], "signal_word": "Danger", "h_statements": ["H225", "H304", "H315", "H336", "H361", "H373"]},
        "sulfuric acid": {"pictograms": ["GHS05"], "signal_word": "Danger", "h_statements": ["H314", "H290"]},
        "hydrogen peroxide (30%)": {"pictograms": ["GHS03", "GHS05", "GHS07", "GHS08"], "signal_word": "Danger", "h_statements": ["H302", "H314", "H318", "H332", "H335"]},
    }

    def classify(self, chemical):
        data = self.HAZARD_DATA.get(chemical.lower())
        if not data:
            return {"chemical": chemical, "classification": "unknown — consult SDS",
                    "pictograms": [], "signal_word": "Unknown"}
        return {
            "chemical": chemical,
            "pictograms": data["pictograms"],
            "pictogram_meanings": [GHS_PICTOGRAMS.get(p, "?") for p in data["pictograms"]],
            "signal_word": data["signal_word"],
            "h_statements": data["h_statements"],
        }

    def pictogram_legend(self):
        return GHS_PICTOGRAMS

    def list_chemicals(self):
        return list(self.HAZARD_DATA.keys())
