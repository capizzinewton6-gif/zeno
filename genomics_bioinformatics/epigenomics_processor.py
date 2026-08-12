"""DNA methylation and ChIP-seq peak analysis."""
from __future__ import annotations

import math


class EpigenomicsProcessor:
    @staticmethod
    def methylation_calls(beta_values: list[float]) -> list[str]:
        """Classify CpG methylation from beta values (0-1)."""
        calls = []
        for b in beta_values:
            if b >= 0.8:
                calls.append("hyper-methylated")
            elif b <= 0.2:
                calls.append("hypo-methylated")
            else:
                calls.append("intermediate")
        return calls

    @staticmethod
    def chipseq_peak_call(reads: list[int], background: float,
                          p_threshold: float = 1e-5) -> list[dict]:
        """Naive Poisson-based peak calling."""
        peaks = []
        for i, count in enumerate(reads):
            lam = max(background, 1e-6)
            # P(X >= count) for Poisson
            p = 1.0 - _poisson_cdf(count - 1, lam)
            if p < p_threshold:
                peaks.append({"bin": i, "reads": count, "p_value": round(p, 8)})
        return peaks

    @staticmethod
    def enrichment_fold(ip: list[float], input_ctrl: list[float]) -> list[float]:
        return [round(ip[i] / max(input_ctrl[i], 1e-9), 4)
                for i in range(len(ip))]

    @staticmethod
    def dmr_call(methyl_a: list[float], methyl_b: list[float],
                 diff_threshold: float = 0.2) -> list[dict]:
        dmrs = []
        for i, (a, b) in enumerate(zip(methyl_a, methyl_b)):
            if abs(a - b) >= diff_threshold:
                dmrs.append({"position": i, "beta_a": round(a, 3),
                             "beta_b": round(b, 3), "delta": round(a - b, 3)})
        return dmrs


def _poisson_cdf(k, lam):
    s = 0.0
    for i in range(int(k) + 1):
        s += math.exp(-lam) * lam ** i / math.factorial(i)
    return min(max(s, 0.0), 1.0)
