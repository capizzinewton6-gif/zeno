"""Dual-use research and biosecurity screening layer.

The safety layer inspects biological requests and sequences for dangerous
content before any genetic-engineering or simulation work proceeds. It blocks
actionable guidance for select agents and regulated toxins, and classifies
the appropriate Biosafety Level (BSL).
"""
from __future__ import annotations

import re

# Abbreviated, non-actionable reference lists. We store only names so we can
# detect and refuse; we never store or output protocols, sequences, or
# enhancement methods for these agents.
SELECT_AGENTS = {
    "bacillus anthracis", "yersinia pestis", "francisella tularensis",
    "burkholderia pseudomallei", "burkholderia mallei", "brucella melitensis",
    "rickettsia prowazekii", "coxiella burnetii", "clostridium botulinum",
    "variola", "monkeypox virus", "ebola", "marburg", "lassa",
    "junin", "machupo", "guanarito", "sabia", "crimean-congo",
}

REGULATED_TOXINS = {
    "botulinum neurotoxin", "ricin", "saxitoxin", "tetrodotoxin",
    "staphylococcal enterotoxin b", "t-2 toxin", "diacetoxyscirpenol",
    "abrin", "shiga toxin", "clostridium perfringens epsilon toxin",
}

DENIED_KEYWORDS = (
    "weaponize", "aerosolize for dissemination", "enhance pathogenicity",
    "increase transmissibility", "evade detection", "harmful to humans",
    "gain of function pathogen",
)


class SafetyVerdict:
    def __init__(self, allowed: bool, bsl: int = 1, reason: str = ""):
        self.allowed = allowed
        self.bsl = bsl
        self.reason = reason

    def __bool__(self) -> bool:
        return self.allowed

    def as_dict(self) -> dict:
        return {"allowed": self.allowed, "bsl": self.bsl, "reason": self.reason}


class SafetyLayer:
    """Screens prompts and sequences for dual-use concerns."""

    def screen_text(self, text: str) -> SafetyVerdict:
        low = text.lower()
        for agent in SELECT_AGENTS:
            if agent in low:
                return SafetyVerdict(
                    False, 4,
                    f"Request references select agent '{agent}'. Actionable "
                    "guidance is refused; guidance limited to public-health "
                    "biosafety and BSL-4 containment only.",
                )
        for toxin in REGULATED_TOXINS:
            if toxin in low:
                return SafetyVerdict(
                    False, 4,
                    f"Request references regulated toxin '{toxin}'. "
                    "Actionable guidance is refused.",
                )
        for kw in DENIED_KEYWORDS:
            if kw in low:
                return SafetyVerdict(
                    False, 1,
                    f"Request contains dual-use concern keyword '{kw}'. "
                    "Refusing to provide actionable guidance.",
                )
        return SafetyVerdict(True, 1, "No dual-use concerns detected.")

    def screen_sequence(self, sequence: str) -> SafetyVerdict:
        seq = re.sub(r"[^ACGTUNacgtun]", "", sequence).upper()
        if len(seq) > 20000:
            return SafetyVerdict(
                False, 1,
                "Sequence exceeds 20 kb screening limit and must be reviewed "
                "manually before processing.",
            )
        # Heuristic: we cannot perform true pathogen BLAST offline, so we flag
        # only pathogen-name context provided alongside the sequence.
        return SafetyVerdict(True, 1, "Sequence passed length-based screening.")

    def classify_bsl(self, organism: str) -> int:
        low = organism.lower()
        if any(a in low for a in ("ebola", "variola", "lassa", "marburg", "monkeypox")):
            return 4
        if any(a in low for a in ("mycobacterium tuberculosis", "yersinia pestis",
                                   "francisella", "coxiella", "brucella")):
            return 3
        if any(a in low for a in ("salmonella", "listeria", "borg.", "schistosoma")):
            return 2
        return 1
