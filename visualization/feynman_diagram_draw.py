"""Render Feynman diagrams for particle interaction channels."""

from __future__ import annotations

from tools.plot_generator import PlotGenerator


class FeynmanDiagramDraw:
    """ASCII / matplotlib renderings of Feynman diagrams."""

    def __init__(self, plotter: PlotGenerator | None = None):
        self.plot = plotter or PlotGenerator()

    def draw(self, ax, channel: str = "s_channel"):
        diagrams = {
            "s_channel": "e- e+ -> gamma* -> mu- mu+",
            "t_channel": "e- mu- -> e- mu-  (photon t-channel)",
            "compton": "gamma e- -> gamma e-  (s + u)",
            "moller": "e- e- -> e- e-  (t + u)",
        }
        ax.text(0.5, 0.5, diagrams.get(channel, "unknown channel"),
                ha="center", va="center", fontsize=12, color="#e6edf3",
                transform=ax.transAxes)
        ax.set_title(f"Feynman diagram: {channel}")
        ax.set_xticks([]); ax.set_yticks([])
        # draw a schematic vertex
        import matplotlib.patches as mp
        ax.add_patch(mp.FancyArrowPatch((0.1, 0.5), (0.45, 0.5), arrowstyle="->", color="#e69f00"))
        ax.add_patch(mp.FancyArrowPatch((0.1, 0.5), (0.45, 0.5), arrowstyle="-", color="#009e73"))
        ax.add_patch(mp.FancyArrowPatch((0.55, 0.5), (0.9, 0.5), arrowstyle="->", color="#e69f00"))

    @staticmethod
    def latex_source(channel: str) -> str:
        from tools.tikz_generator import TikzGenerator
        return TikzGenerator.feynman_diagram(channel[:1])
