"""Natural selection and allele frequency drift."""
from __future__ import annotations

import random


class EvolutionSimulator:
    def run(self, population=1000, generations=100, fitness_advantage=0.05,
             p0=0.01, seed=0) -> dict:
        rng = random.Random(seed)
        p = p0
        history = {"generation": [], "allele_freq": [], "genotype_counts": []}
        for g in range(generations):
            # selection
            w_AA, w_Aa, w_aa = 1.0, 1.0, 1.0 - fitness_advantage
            q = 1 - p
            freq_AA, freq_Aa, freq_aa = p ** 2, 2 * p * q, q ** 2
            mean_w = freq_AA * w_AA + freq_Aa * w_Aa + freq_aa * w_aa
            freq_AA *= w_AA / mean_w
            freq_Aa *= w_Aa / mean_w
            freq_aa *= w_aa / mean_w
            p = freq_AA + 0.5 * freq_Aa
            # genetic drift (binomial sampling)
            k = sum(1 for _ in range(2 * population) if rng.random() < p)
            p = k / (2 * population)
            history["generation"].append(g)
            history["allele_freq"].append(round(p, 5))
            history["genotype_counts"].append({
                "AA": round(freq_AA * population),
                "Aa": round(freq_Aa * population),
                "aa": round(freq_aa * population),
            })
        return {"population": population, "generations": generations,
                "final_freq": round(p, 5), "fixation": p > 0.999 or p < 0.001,
                **history}


class GeneticDriftSimulator:
    def run(self, p0=0.5, ne=100, generations=200, seed=0) -> dict:
        rng = random.Random(seed)
        p = p0
        history = [p]
        for _ in range(generations):
            k = sum(1 for _ in range(2 * ne) if rng.random() < p)
            p = k / (2 * ne)
            history.append(p)
        return {"ne": ne, "generations": generations,
                "final_freq": round(p, 5),
                "fixation": p > 0.999 or p < 0.001,
                "history": [round(h, 4) for h in history]}
