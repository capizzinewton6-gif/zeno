"""Differential gene expression (DESeq2-style)."""
from __future__ import annotations

import math


class RNASeqProcessor:
    @staticmethod
    def normalize_counts(count_matrix: list[list[int]]) -> list[list[float]]:
        """DESeq median-of-ratios normalization."""
        # count_matrix: genes x samples
        n_samples = len(count_matrix[0]) if count_matrix else 0
        sample_means = [0.0] * n_samples
        for row in count_matrix:
            for j in range(n_samples):
                sample_means[j] += math.log(max(row[j], 1))
        size_factors = [math.exp(m / max(len(count_matrix), 1)) for m in sample_means]
        norm = []
        for row in count_matrix:
            norm.append([row[j] / max(size_factors[j], 1e-9) for j in range(n_samples)])
        return norm

    @staticmethod
    def log2_fold_change(control: list[float], treated: list[float]) -> list[float]:
        import numpy as np
        c = np.array(control, dtype=float)
        t = np.array(treated, dtype=float)
        return (np.log2(np.maximum(t, 1)) - np.log2(np.maximum(c, 1))).round(3).tolist()

    @staticmethod
    def differential_expression(control: list[list[float]],
                                treated: list[list[float]]) -> list[dict]:
        """Per-gene t-test-ish score (mean difference + log2FC)."""
        import numpy as np
        c = np.array(control, dtype=float)
        t = np.array(treated, dtype=float)
        results = []
        for i in range(len(c)):
            mean_c = float(np.mean(c[i])) or 1e-9
            mean_t = float(np.mean(t[i]))
            log2fc = math.log2(max(mean_t, 1e-9) / max(mean_c, 1e-9))
            pooled_std = math.sqrt(float(np.var(c[i])) + float(np.var(t[i])) or 1e-9)
            stat = (mean_t - mean_c) / pooled_std
            results.append({"gene_index": i, "log2FC": round(log2fc, 3),
                            "score": round(stat, 3),
                            "regulated": "up" if log2fc > 1 else
                                         "down" if log2fc < -1 else "ns"})
        return results

    @staticmethod
    def pca(matrix: list[list[float]], n_components: int = 2) -> list[list[float]]:
        import numpy as np
        X = np.array(matrix, dtype=float)
        X = X - X.mean(axis=0)
        U, S, Vt = np.linalg.svd(X, full_matrices=False)
        return (U[:, :n_components] * S[:n_components]).round(3).tolist()
