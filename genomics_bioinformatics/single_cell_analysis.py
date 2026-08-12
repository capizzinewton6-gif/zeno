"""Seurat/Scanpy scRNA-seq clustering and UMAPs."""
from __future__ import annotations

import math


class SingleCellAnalysis:
    @staticmethod
    def normalize(data: list[list[int]]) -> list[list[float]]:
        """Library-size (CPM) normalization per cell."""
        out = []
        for cell in data:
            total = sum(cell) or 1
            out.append([c / total * 1e6 for c in cell])
        return out

    @staticmethod
    def log_transform(data: list[list[float]]) -> list[list[float]]:
        return [[math.log1p(v) for v in cell] for cell in data]

    @staticmethod
    def highly_variable_genes(data: list[list[float]], top_n: int = 100) -> list[int]:
        """Pick genes with the largest variance across cells."""
        import numpy as np
        arr = np.array(data, dtype=float)
        var = np.var(arr, axis=0)
        return sorted(range(len(var)), key=lambda i: var[i], reverse=True)[:top_n]

    @staticmethod
    def kmeans_cluster(data: list[list[float]], k: int = 3, max_iter: int = 50) -> list[int]:
        """Minimal k-means clustering of cells."""
        import numpy as np
        rng = __import__("random").Random(0)
        X = np.array(data, dtype=float)
        n = len(X)
        if n == 0:
            return []
        centroids = X[rng.sample(range(n), min(k, n))]
        labels = [0] * n
        for _ in range(max_iter):
            for i, cell in enumerate(X):
                labels[i] = int(np.argmin([np.linalg.norm(cell - c) for c in centroids]))
            new_centroids = []
            for j in range(len(centroids)):
                members = X[[i for i in range(n) if labels[i] == j]]
                new_centroids.append(members.mean(axis=0) if len(members) else centroids[j])
            if np.allclose(new_centroids, centroids):
                break
            centroids = np.array(new_centroids)
        return labels

    @staticmethod
    def umap_sketch(data: list[list[float]], n_neighbors: int = 5) -> list[tuple[float, float]]:
        """A lightweight projection stand-in for UMAP (PCA to 2D)."""
        import numpy as np
        X = np.array(data, dtype=float)
        X = X - X.mean(axis=0)
        if X.shape[1] < 2:
            return [(0.0, 0.0) for _ in range(len(X))]
        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        coords = (U[:, :2] * S[:2]).round(3).tolist()
        return [tuple(c) for c in coords]
