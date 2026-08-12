"""Plot growth curves, qPCR cycles, and phylogenetic trees."""
from __future__ import annotations

import os


class PlotGenerator:
    @staticmethod
    def growth_curve(time, od, title="Growth Curve", save_path=None):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(time, od, "o-", label="OD600")
        ax.set_xlabel("Time (h)"); ax.set_ylabel("OD600")
        ax.set_title(title); ax.legend(); ax.grid(True, alpha=0.3)
        return PlotGenerator._save(fig, save_path)

    @staticmethod
    def qPCR_amplification(cycles, fluorescence, title="qPCR Amplification", save_path=None):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.plot(cycles, fluorescence, "s-", label="Fluorescence (RFU)")
        ax.set_xlabel("Cycle"); ax.set_ylabel("Fluorescence (RFU)")
        ax.set_title(title); ax.legend(); ax.grid(True, alpha=0.3)
        return PlotGenerator._save(fig, save_path)

    @staticmethod
    def phylogenetic_tree(newick, title="Phylogenetic Tree", save_path=None):
        """Plot a radial tree from a Newick string (simple text fallback)."""
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.axis("off")
        ax.text(0.5, 0.5, newick, ha="center", va="center",
                family="monospace", fontsize=8)
        ax.set_title(title)
        return PlotGenerator._save(fig, save_path)

    @staticmethod
    def pcr_plate_map(layout: dict, title="PCR Plate Map", save_path=None):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
        rows, cols = 8, 12
        grid = np.zeros((rows, cols))
        for well, label in layout.items():
            r = ord(well[0]) - 65
            c = int(well[1:]) - 1
            if 0 <= r < rows and 0 <= c < cols:
                grid[r, c] = 1
        fig, ax = plt.subplots()
        ax.imshow(grid, cmap="Pastel1", aspect="auto")
        ax.set_xticks(range(cols))
        ax.set_xticklabels(range(1, cols + 1))
        ax.set_yticks(range(rows))
        ax.set_yticklabels([chr(65 + i) for i in range(rows)])
        ax.set_title(title)
        return PlotGenerator._save(fig, save_path)

    @staticmethod
    def _save(fig, save_path):
        if save_path:
            fig.savefig(save_path, dpi=100, bbox_inches="tight")
            import matplotlib.pyplot as plt
            plt.close(fig)
            return save_path
        import matplotlib.pyplot as plt
        # return figure handle for further use
        return fig
