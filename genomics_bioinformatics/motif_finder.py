"""Identify transcription factor binding motifs."""
from __future__ import annotations

from collections import Counter


class MotifFinder:
    @staticmethod
    def position_weight_matrix(sequences: list[str]) -> dict:
        """Build a PWM (per-position base frequencies)."""
        n = min(len(s) for s in sequences) if sequences else 0
        if n == 0:
            return {"length": 0, "pwm": {}}
        pwm = {base: [0.0] * n for base in "ACGT"}
        for i in range(n):
            col = Counter(s[i].upper() for s in sequences)
            total = sum(col.values()) or 1
            for base in "ACGT":
                pwm[base][i] = round(col[base] / total, 4)
        return {"length": n, "pwm": pwm}

    @staticmethod
    def consensus(pwm: dict) -> str:
        """Infer consensus from a PWM (highest frequency base per position)."""
        if not pwm or "pwm" not in pwm:
            return ""
        length = pwm["length"]
        cons = []
        for i in range(length):
            best_base = max("ACGT", key=lambda b: pwm["pwm"][b][i])
            cons.append(best_base)
        return "".join(cons)

    @staticmethod
    def information_content(pwm: dict) -> list[float]:
        """Per-position information content in bits (max 2)."""
        import math
        ic = []
        for i in range(pwm["length"]):
            h = 0.0
            for base in "ACGT":
                p = pwm["pwm"][base][i]
                if p > 0:
                    h -= p * math.log2(p)
            ic.append(round(2 - h, 4))
        return ic

    @staticmethod
    def scan_sequence(sequence: str, pwm: dict, threshold: float = 0.8) -> list[dict]:
        """Score sliding windows against a PWM."""
        length = pwm["length"]
        if length == 0 or len(sequence) < length:
            return []
        hits = []
        for i in range(len(sequence) - length + 1):
            score = 0.0
            for j in range(length):
                base = sequence[i + j].upper()
                score += pwm["pwm"][base][j]
            norm = score / length
            if norm >= threshold:
                hits.append({"position": i, "score": round(norm, 4),
                             "sequence": sequence[i:i + length]})
        return hits
