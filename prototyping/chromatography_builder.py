"""Chromatography builder — HPLC/GC column and mobile phase selection."""


class ChromatographyBuilder:
    """Recommend chromatographic methods."""

    HPLC_COLUMNS = {
        "reversed_phase_C18": {"use": "nonpolar to moderately polar analytes", "mobile_phase": "water/ACN or water/MeOH"},
        "normal_phase_silica": {"use": "polar analytes", "mobile_phase": "hexane/EtOAc"},
        "HILIC": {"use": "very polar analytes", "mobile_phase": "ACN/water (high organic)"},
        "chiral": {"use": "enantiomer separation", "mobile_phase": "hexane/IPA"},
        "ion_exchange": {"use": "charged species", "mobile_phase": "buffer with salt gradient"},
    }

    GC_COLUMNS = {
        "nonpolar_DB5": {"use": "general nonpolar volatiles", "phase": "5% phenyl methylpolysiloxane"},
        "polar_WAX": {"use": "alcohols, acids, flavors", "phase": "polyethylene glycol"},
        "chiral_cyclodextrin": {"use": "chiral volatiles", "phase": "cyclodextrin derivative"},
    }

    def select_hplc(self, analyte_polarity="moderate", chiral=False, charged=False):
        if chiral:
            return self._pick("chiral")
        if charged:
            return self._pick("ion_exchange")
        if analyte_polarity == "polar":
            return self._pick("HILIC")
        if analyte_polarity == "nonpolar":
            return self._pick("reversed_phase_C18")
        return self._pick("reversed_phase_C18")

    def select_gc(self, analyte_type="general"):
        if analyte_type == "polar":
            return {"column": "polar_WAX", **self.GC_COLUMNS["polar_WAX"]}
        if analyte_type == "chiral":
            return {"column": "chiral_cyclodextrin", **self.GC_COLUMNS["chiral_cyclodextrin"]}
        return {"column": "nonpolar_DB5", **self.GC_COLUMNS["nonpolar_DB5"]}

    def _pick(self, key):
        return {"column": key, **self.HPLC_COLUMNS[key]}
