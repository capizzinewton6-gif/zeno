"""Documentation — generate analytical characterization lists (1H NMR, HRMS summary)."""


class Documentation:
    """Generate characterization documentation."""

    def characterization_summary(self, compound, nmr=None, hrms=None, ir=None, mp=None, optical_rotation=None):
        doc = {
            "compound": compound,
            "characterization": {},
        }
        if nmr:
            doc["characterization"]["NMR"] = nmr
        if hrms:
            doc["characterization"]["HRMS"] = hrms
        if ir:
            doc["characterization"]["IR"] = ir
        if mp:
            doc["characterization"]["melting_point"] = mp
        if optical_rotation:
            doc["characterization"]["optical_rotation"] = optical_rotation
        return doc

    def nmr_table(self, peaks):
        """peaks: list of {shift, mult, integration, assignment}."""
        rows = ["| delta (ppm) | mult | int | assignment |",
                "|---|---|---|---|"]
        for p in peaks:
            rows.append(f"| {p.get('shift','')} | {p.get('mult','')} | {p.get('integration','')} | {p.get('assignment','')} |")
        return "\n".join(rows)

    def experimental_section(self, compound, procedure, yield_pct, characterization):
        return {
            "compound": compound,
            "procedure": procedure,
            "yield": f"{yield_pct}%",
            "characterization": characterization,
            "format": "ACS experimental section",
        }
