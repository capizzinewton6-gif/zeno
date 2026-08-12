"""Safety layer — dual-use research, chemical weapons, and precursor screening.

Screens requests for disallowed content (chemical weapons agents, illicit
drug synthesis, explosives precursor instructions) and flags regulated
precursors for awareness only.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Category 1 — disallowed: synthesis/harmful-use instructions for these
# are blocked. Detection is keyword-based and intentionally conservative.
DISALLOWED_KEYWORDS = [
    "nerve agent",
    "chemical weapon",
    "weaponize",
    "weaponise",
    "sarin",
    "vx",
    "mustard gas",
    "sulfur mustard",
    "ricin",
    "tabun",
    "soman",
    "improvised explosive",
    "methamphetamine synthesis",
    "fentanyl synthesis",
    "clandestine lab",
    "explosive formulation",
    "detonator",
]

# Category 2 — regulated precursors: provide harm-reduction awareness but
# never synthesis instructions for misuse.
REGULATED_PRECURSORS = [
    "ephedrine", "pseudoephedrine", "red phosphorus", "hydriodic acid",
    "sodium cyanide", "potassium cyanide", "thionyl chloride", "phosgene",
    "hydrogen cyanide", "sulfur mustard", "tabun", "soman",
]


class SafetyLayer:
    """Screens prompts for disallowed and regulated chemistry content."""

    def screen(self, prompt):
        if not prompt:
            return {"blocked": False, "flags": [], "regulated": []}
        lower = prompt.lower()
        blocked_terms = [k for k in DISALLOWED_KEYWORDS if k in lower]
        if blocked_terms:
            return {
                "blocked": True,
                "reason": "disallowed_content",
                "terms": blocked_terms,
                "message": (
                    "Request blocked by the safety layer: it appears to seek "
                    "instructions for synthesizing chemical weapons, illicit "
                    "drugs, or explosives. This AI cannot assist with harmful-use "
                    "synthesis. I can discuss general chemistry, safe laboratory "
                    "practice, and legitimate research."
                ),
                "flags": blocked_terms,
                "regulated": [],
            }
        regulated_hits = [k for k in REGULATED_PRECURSORS if re.search(r"\b" + re.escape(k) + r"\b", lower)]
        return {
            "blocked": False,
            "flags": [],
            "regulated": regulated_hits,
            "message": (
                "Note: regulated precursor(s) referenced. Use only in a licensed "
                "facility with appropriate permits, engineering controls, and "
                "waste handling."
            ) if regulated_hits else None,
        }

    def screen_data(self, data):
        """Screen a structured payload's string values."""
        text = " ".join(str(v) for v in (data or {}).values())
        return self.screen(text)
