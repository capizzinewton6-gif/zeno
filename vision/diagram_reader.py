"""Parse circuit diagrams, free-body diagrams, and optical ray tracing (text/structured input)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Circuit:
    components: list[dict] = field(default_factory=list)
    nodes: int = 0


@dataclass
class FreeBody:
    forces: list[dict] = field(default_factory=list)
    object: str = ""


class DiagramReader:
    """Structured-diagram parsers (operate on parsed component lists)."""

    @staticmethod
    def parse_circuit(text: str) -> Circuit:
        """Parse simple 'R=10,X=2' style component descriptions."""
        comps = []
        for tok in text.replace(" ", "").split(","):
            if "=" in tok:
                kind, val = tok.split("=", 1)
                comps.append({"type": kind, "value": val})
        return Circuit(components=comps, nodes=len(set(c["type"] for c in comps)))

    @staticmethod
    def parse_free_body(text: str) -> FreeBody:
        """Parse 'F1=mg,down;F2=N,up' style force lists."""
        forces = []
        for part in text.split(";"):
            if "=" in part:
                mag, info = part.split("=", 1)
                direction = info.split(",")[-1].strip()
                forces.append({"label": mag.strip(), "direction": direction})
        return FreeBody(forces=forces)

    @staticmethod
    def optical_ray(focal_length: float, object_distance: float) -> dict:
        """Thin-lens ray tracing: 1/f = 1/do + 1/di."""
        if object_distance == focal_length:
            return {"image_distance": float("inf"), "magnification": float("inf")}
        di = 1 / (1 / focal_length - 1 / object_distance)
        m = -di / object_distance
        return {"image_distance": di, "magnification": m}
