"""Diagram generator: block, flow, and architecture diagrams."""

from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class DiagramGenerator:
    def block_diagram(self, blocks: list[dict], connections: list[tuple[int, int]],
                      title: str = "Block Diagram", path: str = "block_diagram.png") -> str:
        """blocks: [{name, x, y, w, h}] with x,y in [0,1]."""
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=14, fontweight="bold")
        for blk in blocks:
            rect = mpatches.FancyBboxPatch(
                (blk["x"], blk["y"]), blk.get("w", 0.2), blk.get("h", 0.1),
                boxstyle="round,pad=0.01", linewidth=1.5,
                edgecolor="#2c3e50", facecolor="#3498db", alpha=0.6)
            ax.add_patch(rect)
            ax.text(blk["x"] + blk.get("w", 0.2) / 2,
                    blk["y"] + blk.get("h", 0.1) / 2,
                    blk["name"], ha="center", va="center", fontsize=9)
        for a, b in connections:
            ba, bb = blocks[a], blocks[b]
            ax.annotate("", xy=(bb["x"], bb["y"] + bb.get("h", 0.1) / 2),
                        xytext=(ba["x"] + ba.get("w", 0.2), ba["y"] + ba.get("h", 0.1) / 2),
                        arrowprops=dict(arrowstyle="->", lw=1.5, color="#2c3e50"))
        fig.tight_layout()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path

    def flowchart(self, steps: list[str], title: str = "Flowchart",
                  path: str = "flowchart.png") -> str:
        fig, ax = plt.subplots(figsize=(8, max(6, len(steps) * 0.8)))
        ax.set_xlim(0, 1)
        ax.set_ylim(0, len(steps) + 1)
        ax.axis("off")
        ax.set_title(title, fontsize=14, fontweight="bold")
        h = 0.6
        for i, step in enumerate(steps):
            y = len(steps) - i
            rect = mpatches.FancyBboxPatch(
                (0.3, y - h / 2), 0.4, h,
                boxstyle="round,pad=0.01", linewidth=1.5,
                edgecolor="#2c3e50", facecolor="#27ae60", alpha=0.5)
            ax.add_patch(rect)
            ax.text(0.5, y, step, ha="center", va="center", fontsize=10)
            if i < len(steps) - 1:
                ax.annotate("", xy=(0.5, y - 1 + h / 2), xytext=(0.5, y - h / 2),
                            arrowprops=dict(arrowstyle="->", lw=1.5, color="#2c3e50"))
        fig.tight_layout()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return path
