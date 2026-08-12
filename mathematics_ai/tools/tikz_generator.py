"""Generate LaTeX TikZ and PGFPlots diagrams."""

from __future__ import annotations

from typing import Iterable


def tikz_document(body: str) -> str:
    """Wrap a TikZ body in a standalone document."""
    return (
        "\\documentclass[tikz,border=10pt]{standalone}\n"
        "\\usepackage{tikz}\n"
        "\\begin{document}\n"
        "\\begin{tikzpicture}\n"
        f"{body}\n"
        "\\end{tikzpicture}\n"
        "\\end{document}\n"
    )


def triangle(a: tuple[float, float], b: tuple[float, float], c: tuple[float, float], labels: tuple[str, str, str] = ("A", "B", "C")) -> str:
    la, lb, lc = labels
    body = (
        f"  \\coordinate ({la}) at ({a[0]},{a[1]});\n"
        f"  \\coordinate ({lb}) at ({b[0]},{b[1]});\n"
        f"  \\coordinate ({lc}) at ({c[0]},{c[1]});\n"
        f"  \\draw ({la}) -- ({lb}) -- ({lc}) -- cycle;\n"
        f"  \\node[above left] at ({la}) ${{{la}}}$;\n"
        f"  \\node[above right] at ({lb}) ${{{lb}}}$;\n"
        f"  \\node[below] at ({lc}) ${{{lc}}}$;\n"
    )
    return tikz_document(body)


def pgfplots_function(expr: str, var: str = "x", xmin: float = -5, xmax: float = 5, samples: int = 100) -> str:
    """PGFPlots code plotting y = expr(var)."""
    xlabel = f"${var}$"
    ylabel = f"$f({var})$"
    return (
        "\\documentclass[tikz]{standalone}\n"
        "\\usepackage{pgfplots}\n"
        "\\pgfplotsset{compat=1.18}\n"
        "\\begin{document}\n"
        "\\begin{tikzpicture}\n"
        "\\begin{axis}[\n"
        f"    xlabel={xlabel}, ylabel={ylabel},\n"
        f"    domain={xmin}:{xmax}, samples={samples},\n"
        "    axis lines=middle, grid=both,\n"
        "]\n"
        f"\\addplot[blue, thick] {{{expr}}};\n"
        "\\end{axis}\n"
        "\\end{tikzpicture}\n"
        "\\end{document}\n"
    )


def graph_edges(nodes: Iterable[str], edges: Iterable[tuple[str, str]], layout: str = "spring") -> str:
    """TikZ graph from node labels and edges."""
    node_list = list(nodes)
    edge_list = list(edges)
    body = ""
    # simple circular layout
    import math
    n = len(node_list)
    for i, node in enumerate(node_list):
        angle = 2 * math.pi * i / n if n else 0
        r = 2.0
        body += f"  \\node[circle, draw] ({node}) at ({r * math.cos(angle):.2f},{r * math.sin(angle):.2f}) ${{{node}}}$;\n"
    for u, v in edge_list:
        body += f"  \\draw ({u}) -- ({v});\n"
    return tikz_document(body)


def commutative_diagram(objects: list[str], arrows: list[tuple[str, str, str]]) -> str:
    """TikZ commutative diagram. ``arrows`` are (source, target, label)."""
    body = ""
    for i, obj in enumerate(objects):
        body += f"  \\node ({obj}) at ({i * 3},0) ${{{obj}}}$;\n"
    for src, tgt, label in arrows:
        body += f"  \\draw[->] ({src}) -- node[above] ${{{label}}}$ ({tgt});\n"
    return tikz_document(body)


__all__ = ["tikz_document", "triangle", "pgfplots_function", "graph_edges", "commutative_diagram"]
