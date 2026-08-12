"""Autonomous Painter: controls Microsoft Paint (or a cross-platform
fallback) to create engineering drawings and save them as PNG files.

On Windows this drives ``mspaint.exe`` via ``pyautogui``. On other platforms
it falls back to generating the drawings with matplotlib so the invention
workflow still produces blueprint PNGs without manual drawing.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from typing import List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class PainterAutomation:
    def __init__(self, output_dir: str = "blueprints"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.process = None
        self.platform = os.name
        self._pyautogui = None  # lazy-loaded only on Windows

    # --- Paint process control (Windows) ---------------------------------
    def launch_paint(self) -> bool:
        if self.platform != "nt":
            return False
        mspaint = shutil.which("mspaint") or r"C:\Windows\System32\mspaint.exe"
        if not os.path.exists(mspaint):
            return False
        self.process = subprocess.Popen([mspaint])
        return True

    def _ensure_pyautogui(self):
        if self._pyautogui is None:
            try:
                import pyautogui
                self._pyautogui = pyautogui
            except Exception:
                self._pyautogui = False
        return self._pyautogui

    def close_paint(self):
        if self.process:
            self.process.terminate()
            self.process = None

    # --- Drawing primitives (matplotlib fallback works everywhere) -------
    def _new_canvas(self, title: str = "", size=(8, 6)):
        fig, ax = plt.subplots(figsize=size)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_aspect("equal")
        ax.axis("off")
        if title:
            ax.set_title(title, fontsize=13, fontweight="bold")
        return fig, ax

    def draw_rectangle(self, x: float, y: float, w: float, h: float,
                       label: str = "", path: str = "rect.png",
                       title: str = "") -> str:
        fig, ax = self._new_canvas(title)
        rect = mpatches.Rectangle((x, y), w, h, linewidth=2,
                                  edgecolor="black", facecolor="#aec6cf", alpha=0.5)
        ax.add_patch(rect)
        if label:
            ax.text(x + w / 2, y + h / 2, label, ha="center", va="center")
        return self._save(fig, path)

    def draw_circuit(self, components: List[dict], connections: List[tuple],
                     path: str = "circuit.png", title: str = "Circuit Schematic") -> str:
        fig, ax = self._new_canvas(title)
        for c in components:
            ax.add_patch(mpatches.Rectangle((c["x"], c["y"]), 1.2, 0.6,
                                             edgecolor="black", facecolor="white"))
            ax.text(c["x"] + 0.6, c["y"] + 0.3, c["name"],
                    ha="center", va="center", fontsize=8)
        for a, b in connections:
            ca, cb = components[a], components[b]
            ax.annotate("", xy=(cb["x"], cb["y"] + 0.3),
                        xytext=(ca["x"] + 1.2, ca["y"] + 0.3),
                        arrowprops=dict(arrowstyle="->", color="black"))
        return self._save(fig, path)

    def draw_wiring(self, wires: List[dict], path: str = "wiring.png",
                    title: str = "Wiring Layout") -> str:
        fig, ax = self._new_canvas(title)
        for w in wires:
            xs, ys = w["from"]
            xe, ye = w["to"]
            ax.plot([xs, xe], [ys, ye], color=w.get("color", "red"), lw=2)
            ax.text((xs + xe) / 2, (ys + ye) / 2 + 0.2, w.get("label", ""),
                    fontsize=7, ha="center")
        return self._save(fig, path)

    def draw_blueprint_view(self, view_name: str, shapes: List[dict],
                            path: str | None = None,
                            title: str | None = None) -> str:
        path = path or os.path.join(self.output_dir, f"{view_name}.png")
        title = title or view_name.replace("_", " ").title()
        fig, ax = self._new_canvas(title)
        for s in shapes:
            kind = s.get("kind", "rect")
            if kind == "rect":
                ax.add_patch(mpatches.Rectangle((s["x"], s["y"]), s["w"], s["h"],
                                                edgecolor="black",
                                                facecolor="#cfe2f3", alpha=0.6))
            elif kind == "circle":
                ax.add_patch(mpatches.Circle((s["x"], s["y"]), s["r"],
                                             edgecolor="black",
                                             facecolor="#cfe2f3", alpha=0.6))
            elif kind == "line":
                ax.plot([s["x1"], s["x2"]], [s["y1"], s["y2"]], "k-", lw=2)
            if s.get("label"):
                ax.text(s.get("x", 0), s.get("y", 0) - 0.3, s["label"],
                        ha="center", fontsize=8)
        return self._save(fig, path)

    def generate_all_views(self, shapes_by_view: dict,
                           output_dir: str | None = None) -> list[str]:
        out = output_dir or self.output_dir
        os.makedirs(out, exist_ok=True)
        paths = []
        views = ["front_view", "rear_view", "left_view", "right_view",
                 "top_view", "bottom_view", "isometric_view",
                 "cross_section_view", "exploded_view", "internal_assembly_view",
                 "wiring_layout", "circuit_schematic", "mechanical_assembly",
                 "block_diagram", "system_architecture", "fluid_flow",
                 "manufacturing_drawing"]
        for view in views:
            shapes = shapes_by_view.get(view, shapes_by_view.get("default", []))
            paths.append(self.draw_blueprint_view(view, shapes,
                         path=os.path.join(out, f"{view}.png")))
        return paths

    def _save(self, fig, path: str) -> str:
        # If path is already absolute or already nests under output_dir, use
        # it as-is; otherwise place it inside output_dir.
        if os.path.isabs(path) or (self.output_dir and path.startswith(self.output_dir + os.sep)):
            full = path
        else:
            full = os.path.join(self.output_dir, path)
        os.makedirs(os.path.dirname(full) or ".", exist_ok=True)
        fig.savefig(full, dpi=120, bbox_inches="tight")
        plt.close(fig)
        return full
