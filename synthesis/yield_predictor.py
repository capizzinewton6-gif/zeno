"""Yield predictor — predict reaction yields and side-product formation."""


class YieldPredictor:
    """Heuristic reaction-yield estimation."""

    BASELINE_YIELDS = {
        "Suzuki": 85, "Grignard": 70, "esterification": 75,
        "amide_coupling": 80, "hydrogenation": 90, "Diels-Alder": 82,
        "Wittig": 65, "Friedel-Crafts": 60, "SN2": 78,
    }

    SIDE_PRODUCT_RISKS = {
        "Sukuki": ["homocoupling", "deborylation"],
        "Grignard": ["Wurtz coupling", "reduction"],
        "esterification": ["over-esterification", "dehydration"],
        "amide_coupling": ["racemization", "urea formation"],
        "hydrogenation": ["over-reduction", "catalyst poisoning"],
    }

    def predict(self, reaction_type, temperature_C=25, equivalents=1.0, catalyst_loading=0.05):
        base = self.BASELINE_YIELDS.get(reaction_type, 70)
        # Simple heuristics: high T penalty, excess reagent bonus, low catalyst penalty
        t_penalty = max(0, (temperature_C - 80) * 0.2)
        equiv_bonus = min(8, (equivalents - 1) * 5) if equivalents > 1 else 0
        cat_penalty = max(0, (0.05 - catalyst_loading) * 100)
        predicted = max(0, min(99, base - t_penalty + equiv_bonus - cat_penalty))
        return {
            "reaction_type": reaction_type,
            "predicted_yield_pct": round(predicted, 1),
            "base_yield": base,
            "adjustments": {"temp_penalty": round(t_penalty, 2),
                            "equiv_bonus": round(equiv_bonus, 2),
                            "catalyst_penalty": round(cat_penalty, 2)},
            "side_product_risks": self.SIDE_PRODUCT_RISKS.get(reaction_type, []),
            "note": "Heuristic estimate; verify experimentally.",
        }
