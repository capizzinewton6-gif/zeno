"""Graph theory, enumeration and extremal combinatorics."""

from __future__ import annotations

from itertools import combinations, permutations
from typing import Any

import networkx as nx
import math


# --- enumeration ----------------------------------------------------
def factorial(n: int) -> int:
    return math.factorial(n)


def binomial(n: int, k: int) -> int:
    return math.comb(n, k)


def permutations_count(n: int, k: int | None = None) -> int:
    if k is None:
        return math.factorial(n)
    return math.perm(n, k)


def permutations_list(items: list[Any], k: int | None = None) -> list[tuple[Any, ...]]:
    return list(permutations(items, k)) if k else list(permutations(items))


def combinations_list(items: list[Any], k: int) -> list[tuple[Any, ...]]:
    return list(combinations(items, k))


def stirling_second(n: int, k: int) -> int:
    """Stirling number of the second kind S(n,k)."""
    if n == k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return k * stirling_second(n - 1, k) + stirling_second(n - 1, k - 1)


def bell_number(n: int) -> int:
    """Bell number B_n: number of partitions of an n-element set."""
    return sum(stirling_second(n, k) for k in range(n + 1))


# --- graph theory ---------------------------------------------------
def complete_graph(n: int) -> nx.Graph:
    return nx.complete_graph(n)


def random_erdos_renyi(n: int, p: float, seed: int | None = None) -> nx.Graph:
    return nx.erdos_renyi_graph(n, p, seed=seed)


def graph_properties(g: nx.Graph) -> dict[str, Any]:
    return {
        "nodes": g.number_of_nodes(),
        "edges": g.number_of_edges(),
        "connected": nx.is_connected(g) if g.number_of_nodes() > 0 else False,
        "components": nx.number_connected_components(g),
        "is_bipartite": nx.is_bipartite(g),
        "is_planar": nx.check_planarity(g)[0] if g.number_of_nodes() <= 100 else None,
        "chromatic_number": chromatic_number(g),
        "diameter": nx.diameter(g) if nx.is_connected(g) and g.number_of_nodes() > 1 else None,
        "is_eulerian": nx.is_eulerian(g),
    }


def chromatic_number(g: nx.Graph) -> int:
    """Greedy upper bound then verify with increasing k via DSatur-like search."""
    if g.number_of_nodes() == 0:
        return 0
    # greedy coloring
    coloring = nx.greedy_color(g, strategy="DSATUR")
    return max(coloring.values()) + 1 if coloring else 0


def handshaking_check(g: nx.Graph) -> bool:
    """Sum of degrees = 2 * |E|."""
    return sum(dict(g.degree()).values()) == 2 * g.number_of_edges()


def shortest_path(g: nx.Graph, source: Any, target: Any) -> list[Any]:
    return nx.shortest_path(g, source=source, target=target)


def spanning_tree_count(g: nx.Graph) -> int:
    """Number of spanning trees via Kirchhoff's Matrix-Tree theorem."""
    import numpy as np
    n = g.number_of_nodes()
    if n == 0:
        return 0
    if n == 1:
        return 1
    L = nx.laplacian_matrix(g).toarray().astype(float)
    minor = L[:-1, :-1]
    return int(round(np.linalg.det(minor)))


__all__ = [
    "factorial", "binomial", "permutations_count", "permutations_list",
    "combinations_list", "stirling_second", "bell_number", "complete_graph",
    "random_erdos_renyi", "graph_properties", "chromatic_number",
    "handshaking_check", "shortest_path", "spanning_tree_count",
]
