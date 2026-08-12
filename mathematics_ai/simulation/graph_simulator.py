"""Random graphs (Erdős–Rényi), network growth and spectral graph theory."""

from __future__ import annotations

from typing import Any

import numpy as np
import networkx as nx


def erdos_renyi(n: int, p: float, seed: int | None = None) -> nx.Graph:
    return nx.erdos_renyi_graph(n, p, seed=seed)


def watts_strogatz(n: int, k: int, p: float, seed: int | None = None) -> nx.Graph:
    return nx.watts_strogatz_graph(n, k, p, seed=seed)


def barabasi_albert(n: int, m: int, seed: int | None = None) -> nx.Graph:
    return nx.barabasi_albert_graph(n, m, seed=seed)


def preferential_attachment_grow(g: nx.Graph, new_nodes: int, m: int, seed: int | None = None) -> nx.Graph:
    """Grow an existing graph by preferential attachment."""
    rng = np.random.default_rng(seed)
    g = g.copy()
    next_id = max(g.nodes()) + 1 if g.nodes else 0
    for _ in range(new_nodes):
        if g.number_of_edges() == 0:
            targets = list(range(min(m, next_id)))
        else:
            degrees = np.array([g.degree(n) for n in g.nodes()], dtype=float)
            probs = degrees / degrees.sum() if degrees.sum() else None
            targets = rng.choice(list(g.nodes()), size=m, replace=False, p=probs)
        for t in targets:
            g.add_edge(next_id, int(t))
        next_id += 1
    return g


def graph_spectral_properties(g: nx.Graph) -> dict[str, list]:
    """Eigenvalues of the adjacency and Laplacian matrices."""
    A = nx.adjacency_matrix(g).toarray().astype(float)
    L = nx.laplacian_matrix(g).toarray().astype(float)
    return {
        "adjacency_eigenvalues": np.linalg.eigvalsh(A).tolist(),
        "laplacian_eigenvalues": np.linalg.eigvalsh(L).tolist(),
    }


def small_world_coefficient(g: nx.Graph) -> float:
    """Small-world sigma = (C/C_rand) / (L/L_rand)."""
    if g.number_of_nodes() < 2:
        return 0.0
    n = g.number_of_nodes()
    k_avg = 2 * g.number_of_edges() / n
    p = k_avg / max(n - 1, 1)
    rand = erdos_renyi(n, p)
    C = nx.average_clustering(g)
    C_rand = nx.average_clustering(rand)
    if not nx.is_connected(g):
        sub = g.subgraph(max(nx.connected_components(g), key=len))
        L = nx.average_shortest_path_length(sub)
    else:
        L = nx.average_shortest_path_length(g)
    if not nx.is_connected(rand):
        sub = rand.subgraph(max(nx.connected_components(rand), key=len))
        L_rand = nx.average_shortest_path_length(sub)
    else:
        L_rand = nx.average_shortest_path_length(rand)
    if C_rand == 0 or L_rand == 0:
        return 0.0
    return (C / C_rand) / (L / L_rand)


def degree_distribution(g: nx.Graph) -> dict[int, int]:
    degrees = dict(g.degree())
    dist: dict[int, int] = {}
    for d in degrees.values():
        dist[d] = dist.get(d, 0) + 1
    return dist


def percolation_threshold_erdos_renyi(n: int) -> float:
    """Theoretical percolation threshold p_c = 1/n for ER graph."""
    return 1.0 / n


__all__ = [
    "erdos_renyi", "watts_strogatz", "barabasi_albert", "preferential_attachment_grow",
    "graph_spectral_properties", "small_world_coefficient", "degree_distribution",
    "percolation_threshold_erdos_renyi",
]
