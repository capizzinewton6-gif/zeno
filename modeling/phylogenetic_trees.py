"""Cladograms and evolutionary tree models."""
from __future__ import annotations

from calculations.phylogenetics_calc import jukes_cantor_distance, upgma


class PhylogeneticTree:
    @staticmethod
    def distance_matrix_from_alignments(sequences: list[str]) -> list[list[float]]:
        n = len(sequences)
        mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                p = _p_distance(sequences[i], sequences[j])
                d = jukes_cantor_distance(p)
                mat[i][j] = mat[j][i] = round(d, 4)
        return mat

    @staticmethod
    def build_upgma(sequences: list[str], labels: list[str]) -> dict:
        mat = PhylogeneticTree.distance_matrix_from_alignments(sequences)
        return upgma(mat, labels)

    @staticmethod
    def newick(tree_tuple, heights=None) -> str:
        def recurse(node):
            if isinstance(node, str):
                return node
            if len(node) == 1:
                return node[0]
            # split roughly in half
            mid = len(node) // 2
            left, right = node[:mid], node[mid:]
            return f"({recurse(left)},{recurse(right)})"
        return recurse(tree_tuple) + ";"

    @staticmethod
    def from_distance_matrix(matrix, labels):
        return upgma(matrix, labels)


def _p_distance(s1, s2):
    length = min(len(s1), len(s2))
    if length == 0:
        return 0.0
    diffs = sum(a != b for a, b in zip(s1[:length], s2[:length]))
    return diffs / length
