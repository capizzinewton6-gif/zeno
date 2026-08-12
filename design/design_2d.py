"""2D engineering design: generates 2D technical drawings using matplotlib."""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Circle, FancyArrow  # noqa: E402

from src.gemini_25_flash_engine import Gemini25FlashEngine  # noqa: E402


class Design2D:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def describe_view(self, concept: str, view: str) -> str:
        return self.engine.generate(
            f"Describe the {view} 2D engineering view of: {concept}. "
            f"List shapes, positions, and dimensions.",
            system="You are a drafting engineer.")

    def render(self, shapes: list[dict], path: str, title: str = "2D Design",
               width: float = 8, height: float = 6):
        fig, ax = plt.subplots(figsize=(width, height))
        for s in shapes:
            kind = s.get("kind", "rect")
            if kind == "rect":
                ax.add_patch(Rectangle((s["x"], s["y"]), s["w"], s["h"],
                                       fill=False, edgecolor="black", linewidth=1.5))
            elif kind == "circle":
                ax.add_patch(Circle((s["x"], s["y"]), s["r"],
                                    fill=False, edgecolor="black", linewidth=1.5))
            elif kind == "arrow":
                ax.add_patch(FancyArrow(s["x"], s["y"], s["dx"], s["dy"],
                                        width=0.02, length_includes_head=True,
                                        color="black"))
            if "label" in s:
                ax.text(s.get("x", 0), s.get("y", 0), s["label"], fontsize=8)
        ax.set_aspect("equal")
        ax.autoscale()
        ax.set_title(title)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path
