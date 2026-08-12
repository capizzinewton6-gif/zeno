"""Technical drawing: standard multi-view engineering drawings."""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.gemini_25_flash_engine import Gemini25FlashEngine  # noqa: E402


class TechnicalDrawing:
    def __init__(self, engine: Gemini25FlashEngine | None = None):
        self.engine = engine or Gemini25FlashEngine()

    def describe(self, concept: str) -> str:
        return self.engine.generate(
            f"Produce a technical drawing specification (views, dimensions, "
            f"tolerances, annotations) for: {concept}",
            system="You are a technical drafter following ASME Y14.5.")

    def render_multiview(self, views: dict[str, list[dict]], path: str,
                         title: str = "Technical Drawing"):
        n = len(views)
        fig, axes = plt.subplots(1, n, figsize=(5 * n, 5))
        if n == 1:
            axes = [axes]
        from matplotlib.patches import Rectangle, Circle
        for ax, (name, shapes) in zip(axes, views.items()):
            ax.set_title(name)
            for s in shapes:
                if s.get("kind") == "rect":
                    ax.add_patch(Rectangle((s["x"], s["y"]), s["w"], s["h"],
                                           fill=False, edgecolor="black"))
                elif s.get("kind") == "circle":
                    ax.add_patch(Circle((s["x"], s["y"]), s["r"],
                                        fill=False, edgecolor="black"))
            ax.set_aspect("equal")
            ax.autoscale()
        fig.suptitle(title)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return path
