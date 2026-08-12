"""Generate LaTeX TikZ code for optics, circuits, and Feynman diagrams."""

from __future__ import annotations


class TikzGenerator:
    """Emit standalone TikZ snippets (no external compilation needed to view source)."""

    @staticmethod
    def optics_ray_diagram(title: str = "Optical Ray Diagram") -> str:
        return (
            r"\begin{tikzpicture}"
            r"\draw[->] (0,0) -- (6,0) node[right]{optical axis};"
            r"\draw[thick] (2,-1.5) -- (2,1.5) node[above]{lens};"
            r"\draw[->,red] (0,0.8) -- (2,0) -- (5,-0.8);"
            r"\end{tikzpicture}"
        )

    @staticmethod
    def circuit_rc(title: str = "RC Circuit") -> str:
        return (
            r"\begin{tikzpicture}[american]"
            r"\draw (0,0) to[R,l=$R$] (2,0) to[C,l=$C$] (4,0) -- (4,-1) -- (0,-1) -- (0,0);"
            r"\draw (0,0) to[V=$V$] (0,-1);"
            r"\end{tikzpicture}"
        )

    @staticmethod
    def feynman_diagram(channel: str = "s") -> str:
        """Return TikZ-Feynman-ish ASCII-safe source for a simple vertex."""
        if channel == "s":
            return (
                r"\begin{tikzpicture}"
                r"\draw[fermion] (0,0) -- (2,1);"
                r"\draw[fermion] (2,1) -- (4,0);"
                r"\draw[photon] (2,1) -- (2,3);"
                r"\draw[fermion] (0,4) -- (2,3);"
                r"\draw[fermion] (2,3) -- (4,4);"
                r"\end{tikzpicture}"
            )
        return ""
