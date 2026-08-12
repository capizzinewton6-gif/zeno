"""Taxonomic profiling of microbial communities."""
from __future__ import annotations

from collections import Counter


TAXONOMIC_RANKS = ["domain", "phylum", "class", "order", "family", "genus", "species"]


class MetagenomicsEngine:
    @staticmethod
    def alpha_diversity(species_counts: list[int]) -> dict:
        from biology.ecology import EcologyModule
        return {
            "richness": EcologyModule.species_richness(species_counts),
            "shannon": round(EcologyModule.shannon_index(species_counts), 4),
            "simpson": round(EcologyModule.simpson_index(species_counts), 4),
        }

    @staticmethod
    def beta_diversity_unifrac(communities: list[list[int]]) -> list[list[float]]:
        """Bray-Curtis dissimilarity between communities."""
        n = len(communities)
        mat = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                s_ij = sum(min(a, b) for a, b in zip(communities[i], communities[j]))
                s_i = sum(communities[i])
                s_j = sum(communities[j])
                bc = 1 - 2 * s_ij / max(s_i + s_j, 1)
                mat[i][j] = mat[j][i] = round(bc, 4)
        return mat

    @staticmethod
    def taxonomic_profile(read_assignments: list[str]) -> dict:
        counts = Counter(read_assignments)
        total = sum(counts.values()) or 1
        return {"total_reads": sum(counts.values()),
                "profile": {k: round(v / total, 4) for k, v in counts.most_common()},
                "n_taxa": len(counts)}

    @staticmethod
    def core_microbiome(samples: list[dict], threshold: float = 0.8) -> list[str]:
        """Taxa present in >= threshold fraction of samples."""
        from collections import Counter
        presence = Counter()
        for sample in samples:
            for taxon in sample:
                presence[taxon] += 1
        n = len(samples) or 1
        return [t for t, c in presence.items() if c / n >= threshold]
