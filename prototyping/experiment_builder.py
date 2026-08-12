"""Experiment builder — wet-lab synthetic protocols and benchtop procedures."""


class ExperimentBuilder:
    """Build structured experimental protocols."""

    def build(self, title, objective, reagents, procedure, safety_notes=None,
              characterization=None, duration_min=None):
        return {
            "title": title,
            "objective": objective,
            "reagents": reagents,
            "procedure": procedure,
            "safety_notes": safety_notes or [],
            "characterization": characterization or [],
            "estimated_duration_min": duration_min,
            "format": "ELN-ready protocol",
        }

    def from_template(self, template_name, **kwargs):
        templates = {
            "esterification": {
                "title": "Fischer Esterification",
                "objective": "Synthesize ester from carboxylic acid and alcohol",
                "reagents": ["carboxylic acid", "alcohol", "H2SO4 (cat.)"],
                "procedure": ["Combine acid and alcohol", "Add catalytic H2SO4",
                              "Reflux 4 h with Dean-Stark", "Workup and distill"],
                "safety_notes": ["Concentrated acid — wear PPE", "Flammable alcohol"],
            },
            "amide_coupling": {
                "title": "Amide Coupling",
                "objective": "Form amide from acid and amine",
                "reagents": ["carboxylic acid", "amine", "HATU", "DIPEA"],
                "procedure": ["Dissolve acid in DMF", "Add HATU and DIPEA",
                              "Add amine, stir 2 h", "Aqueous workup, chromatography"],
                "safety_notes": ["HATU is a sensitizer", "DMF reproductive hazard"],
            },
        }
        base = templates.get(template_name)
        if not base:
            return {"error": f"Unknown template: {template_name}"}
        base.update(kwargs)
        return self.build(**base)
