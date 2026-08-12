"""3D engineering design: generates 3D representations using matplotlib."""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from src.gemini_25_flash_engine import Gemini25FlashEngine  # noqa: E402


class Design3D:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def describe_view(self, concept: str, view: str) -> str:
        return self.engine.generate(
            f"Describe the {view} 3D representation of: {concept}. "
            f"List primitives, dimensions, and assembly.",
            system="You are a 3D CAD engineer.")

    def render_isometric(self, boxes: list[dict], path: str, title: str = "Isometric View"):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection="3d")
        for b in boxes:
            x, y, z = b["x"], b["y"], b["z"]
            dx, dy, dz = b["dx"], b["dy"], b["dz"]
            color = b.get("color", "lightblue")
            cx = [x, x + dx, x + dx, x, x, x + dx, x + dx, x]
            cy = [y, y, y + dy, y + dy, y, y, y + dy, y + dy]
            cz = [z, z, z, z, z + dz, z + dz, z + dz, z + dz]
            # Draw 12 edges of the box.
            edges = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),
                     (0,4),(1,5),(2,6),(3,7)]
            for a, e in edges:
                ax.plot([cx[a], cx[e]], [cy[a], cy[e]], [cz[a], cz[e]],
                        color="black", linewidth=1)
            ax.bar3d(x, y, z, dx, dy, dz, color=color, alpha=0.4)
        ax.set_title(title)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path

    def render_exploded(self, boxes: list[dict], path: str, gap: float = 0.5,
                        title: str = "Exploded View"):
        offset = []
        cum = 0.0
        for b in boxes:
            offset.append(cum)
            cum += b["dz"] + gap
        exploded = [{**b, "z": b["z"] + off} for b, off in zip(boxes, offset)]
        return self.render_isometric(exploded, path, title)
