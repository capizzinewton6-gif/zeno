"""Toxicity screening — QSAR toxicological modeling and bioaccumulation."""


class ToxicityScreening:
    """Simple QSAR-style toxicity estimators."""

    @staticmethod
    def lipinski_rule_of_5(mw, logp, hbd, hba):
        violations = []
        if mw > 500:
            violations.append("MW > 500")
        if logp > 5:
            violations.append("LogP > 5")
        if hbd > 5:
            violations.append("HBD > 5")
        if hba > 10:
            violations.append("HBA > 10")
        return {"passes": len(violations) == 0, "violations": violations,
                "oral_bioavailability_likely": len(violations) <= 1}

    @staticmethod
    def bioconcentration_factor(logp):
        """BCF ≈ 10^logP (simplified). Log BCF > 3.7 indicates bioaccumulative."""
        import math
        bcf = 10 ** logp
        return {"BCF": round(bcf, 1), "log_BCF": round(logp, 2),
                "bioaccumulative": logp >= 3.7}

    @staticmethod
    def lc50_fish_estimate(logp):
        """Very rough ECOSAR-style estimate: LC50 ~ 10^(-a*logP + b)."""
        import math
        # Simplified neutral organic SAR for fish
        lc50_mg_L = 10 ** (-0.6 * logp + 1.5)
        category = "very toxic" if lc50_mg_L < 1 else "toxic" if lc50_mg_L < 10 else "harmful" if lc50_mg_L < 100 else "low toxicity"
        return {"estimated_LC50_mg_L": round(lc50_mg_L, 3), "category": category,
                "note": "Rough QSAR estimate; verify with experimental data."}

    @staticmethod
    def alert_structures(smiles):
        """Flag common toxicophores by substring matching (illustrative)."""
        alerts = []
        s = (smiles or "").lower()
        patterns = {
            "nitroso": "n=o",
            "azide": "n=[n+]=[n-]",
            "epoxide": "c1oc1",
            "isocyanate": "n=c=o",
            "alpha,beta-unsaturated carbonyl": "c=cc=O".lower(),
        }
        for name, pat in patterns.items():
            if pat in s:
                alerts.append(name)
        return {"alerts": alerts, "n_alerts": len(alerts)}
