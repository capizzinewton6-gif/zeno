"""Plot generator: precision-recall, confusion matrices, latency charts."""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np


class PlotGenerator:
    """Render ASCII charts (matplotlib optional) for quick CLI inspection."""

    @staticmethod
    def precision_recall(precisions: List[float], recalls: List[float]) -> str:
        if not precisions:
            return "no data"
        lines = ["Precision-Recall:"]
        for p, r in zip(precisions, recalls):
            bar_p = "#" * int(p * 20)
            bar_r = "=" * int(r * 20)
            lines.append(f"P {p:.2f} {bar_p:<20}  R {r:.2f} {bar_r:<20}")
        return "\n".join(lines)

    @staticmethod
    def confusion_matrix(matrix: List[List[int]], labels: Optional[List[str]] = None) -> str:
        if not matrix:
            return "empty"
        n = len(matrix)
        labels = labels or [str(i) for i in range(n)]
        col_w = max(6, max(len(l) for l in labels) + 1)
        header = " " * col_w + "".join(f"{l:>{col_w}}" for l in labels)
        lines = [header]
        for i, row in enumerate(matrix):
            lines.append(f"{labels[i]:<{col_w}}" + "".join(f"{v:>{col_w}}" for v in row))
        return "\n".join(lines)

    @staticmethod
    def latency_chart(latencies_ms: List[float]) -> str:
        if not latencies_ms:
            return "no data"
        arr = np.asarray(latencies_ms)
        mean = float(arr.mean())
        p95 = float(np.percentile(arr, 95))
        p99 = float(np.percentile(arr, 99))
        scale = 40.0 / max(arr.max(), 1e-6)
        lines = [f"Latency (ms): mean={mean:.1f} p95={p95:.1f} p99={p99:.1f}"]
        for v in arr:
            lines.append(f"{v:6.1f} | " + "#" * int(v * scale))
        return "\n".join(lines)
