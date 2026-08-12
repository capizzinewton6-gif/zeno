"""Engineering graph generator using matplotlib."""

from __future__ import annotations

import os
from typing import List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class GraphGenerator:
    def __init__(self):
        plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")

    def line(self, x: list, y: list, title: str = "", xlabel: str = "",
             ylabel: str = "", path: str = "graph.png",
             labels: list[str] | None = None) -> str:
        fig, ax = plt.subplots(figsize=(8, 5))
        if isinstance(y[0], list):
            for i, ys in enumerate(y):
                ax.plot(x, ys, label=(labels[i] if labels and i < len(labels) else f"Series {i+1}"))
            ax.legend()
        else:
            ax.plot(x, y)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        fig.tight_layout()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=120)
        plt.close(fig)
        return path

    def scatter(self, x: list, y: list, title: str = "", path: str = "scatter.png") -> str:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(x, y)
        ax.set_title(title)
        fig.tight_layout()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=120)
        plt.close(fig)
        return path

    def bar(self, labels: list[str], values: list[float], title: str = "",
            path: str = "bar.png") -> str:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(labels, values)
        ax.set_title(title)
        fig.tight_layout()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        fig.savefig(path, dpi=120)
        plt.close(fig)
        return path
