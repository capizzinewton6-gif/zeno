"""Analyze physical apparatus diagrams and laboratory optics schematics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class OpticalSetup:
    elements: list[dict] = field(default_factory=list)
    notes: str = ""


class ExperimentalSetupReader:
    """Parse text descriptions of optical / experimental apparatus."""

    @staticmethod
    def parse_optics(text: str) -> OpticalSetup:
        elements = []
        for line in text.splitlines():
            low = line.lower().strip()
            if not low:
                continue
            kind = None
            if "laser" in low: kind = "laser"
            elif "lens" in low: kind = "lens"
            elif "mirror" in low: kind = "mirror"
            elif "beam splitter" in low: kind = "beam_splitter"
            elif "detector" in low: kind = "detector"
            elif "sample" in low: kind = "sample"
            if kind:
                elements.append({"kind": kind, "raw": line.strip()})
        return OpticalSetup(elements=elements)

    @staticmethod
    def trace_path(setup: OpticalSetup) -> list[str]:
        return [e["kind"] for e in setup.elements]
