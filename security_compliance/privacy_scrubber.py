"""Anonymizes internal paths, private URLs, and IP addresses.

Used before sending context to external models or sharing diagnostics. Removes
or replaces sensitive local identifiers with neutral placeholders.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ScrubResult:
    scrubbed: str
    replacements: list[tuple[str, str]] = field(default_factory=list)


class PrivacyScrubber:
    """Replaces PII-like local identifiers with placeholders."""

    PATTERNS: list[tuple[str, str, str]] = [
        # (name, regex, replacement)
        ("absolute_path", r"/(?:home|Users|root|workspace|opt|var)/[\w./\-]+", "<path>"),
        ("ipv4", r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "<ip>"),
        ("ipv6", r"\b[0-9a-fA-F:]{2,5}::?[0-9a-fA-F:]+\b", "<ip>"),
        ("email", r"[\w.+-]+@[\w-]+\.[\w.-]+", "<email>"),
        ("private_url", r"https?://(?:localhost|127\.0\.0\.1|0\.0\.0\.0|10\.|192\.168\.)[^\s'\"]*", "<url>"),
        ("username", r"/(?:home|Users)/([a-zA-Z0-9_.-]+)/", "/home/<user>/"),
        ("mac_address", r"\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b", "<mac>"),
    ]

    def scrub(self, text: str) -> ScrubResult:
        scrubbed = text
        replacements: list[tuple[str, str]] = []
        for name, pattern, replacement in self.PATTERNS:
            def _sub(m, r=replacement, n=name):
                return r
            new, n = re.subn(pattern, replacement, scrubbed)
            if n:
                replacements.append((name, f"{n} occurrence(s)"))
                scrubbed = new
        return ScrubResult(scrubbed=scrubbed, replacements=replacements)

    def scrub_file(self, path: str) -> ScrubResult:
        try:
            with open(path, encoding="utf-8") as f:
                return self.scrub(f.read())
        except OSError:
            return ScrubResult(scrubbed="")
