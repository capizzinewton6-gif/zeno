"""Formula engine — exact masses, molecular weights, isotopic distributions."""

import re


# Monoisotopic and average atomic masses for common elements.
_MONO = {
    "H": 1.007825, "C": 12.000000, "N": 14.003074, "O": 15.994915,
    "F": 18.998403, "Na": 22.989769, "Mg": 23.985042, "P": 30.973762,
    "S": 31.972071, "Cl": 34.968853, "K": 38.963707, "Br": 78.918338,
    "I": 126.904473, "Fe": 55.934938, "Cu": 62.929598, "Zn": 63.929145,
    "Ca": 39.962591, "B": 11.009305, "Li": 7.016004,
}
_AVG = {
    "H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999,
    "F": 18.998, "Na": 22.990, "Mg": 24.305, "P": 30.974,
    "S": 32.06, "Cl": 35.45, "K": 39.098, "Br": 79.904,
    "I": 126.904, "Fe": 55.845, "Cu": 63.546, "Zn": 65.38,
    "Ca": 40.078, "B": 10.81, "Li": 6.94,
}


class FormulaEngine:
    """Parse chemical formulas and compute masses."""

    _TOKEN = re.compile(r"([A-Z][a-z]?)(\d*)")

    @classmethod
    def parse_formula(cls, formula):
        """Return dict of element->count."""
        counts = {}
        for elem, num in cls._TOKEN.findall(formula):
            if not elem:
                continue
            counts[elem] = counts.get(elem, 0) + (int(num) if num else 1)
        return counts

    @classmethod
    def monoisotopic_mass(cls, formula):
        counts = cls.parse_formula(formula)
        return sum(counts[el] * _MONO[el] for el in counts if el in _MONO)

    @classmethod
    def average_mass(cls, formula):
        counts = cls.parse_formula(formula)
        return sum(counts[el] * _AVG[el] for el in counts if el in _AVG)

    @classmethod
    def molecular_weight(cls, formula):
        return cls.average_mass(formula)

    @classmethod
    def isotopic_distribution(cls, formula):
        """Approximate M, M+1, M+2 intensities based on C, S, Cl, Br content."""
        counts = cls.parse_formula(formula)
        c = counts.get("C", 0)
        s = counts.get("S", 0)
        cl = counts.get("Cl", 0)
        br = counts.get("Br", 0)
        m1 = c * 0.0107 + s * 0.0076
        m2 = 0.5 * (c * 0.0107) ** 2 + s * 0.0421 + cl * 0.3198 + br * 0.9731
        return {
            "M": 100.0,
            "M+1": round(m1 * 100, 2),
            "M+2": round(m2 * 100, 2),
        }

    @classmethod
    def degree_of_unsaturation(cls, formula):
        """DBE = C + 1 - H/2 + N/2 - X/2."""
        c = cls.parse_formula(formula)
        C = c.get("C", 0)
        H = c.get("H", 0)
        N = c.get("N", 0)
        X = c.get("F", 0) + c.get("Cl", 0) + c.get("Br", 0) + c.get("I", 0)
        return C + 1 - H / 2 + N / 2 - X / 2

    @classmethod
    def percent_composition(cls, formula):
        counts = cls.parse_formula(formula)
        total = sum(counts[el] * _AVG[el] for el in counts if el in _AVG)
        return {el: round(counts[el] * _AVG[el] / total * 100, 2) for el in counts if el in _AVG}
