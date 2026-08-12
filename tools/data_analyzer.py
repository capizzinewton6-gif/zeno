"""Analyze RNA-seq matrices and plate reader data."""
from __future__ import annotations

import math

from genomics_bioinformatics.rnaseq_processor import RNASeqProcessor


class DataAnalyzer:
    @staticmethod
    def rnaseq_matrix(counts: list[list[int]], gene_names: list[str] | None = None,
                      control_cols: list[int] | None = None,
                      treated_cols: list[int] | None = None) -> dict:
        control_cols = control_cols or [0]
        treated_cols = treated_cols or [1]
        normalized = RNASeqProcessor.normalize_counts(counts)
        control = [[row[c] for c in control_cols] for row in normalized]
        treated = [[row[t] for t in treated_cols] for row in normalized]
        de = RNASeqProcessor.differential_expression(control, treated)
        if gene_names:
            for i, name in enumerate(gene_names):
                if i < len(de):
                    de[i]["gene"] = name
        return {"n_genes": len(de), "differential_expression": de,
                "significant": [d for d in de if d["regulated"] != "ns"]}

    @staticmethod
    def plate_reader_analysis(plate: list[list[float]], blank_wells: list[tuple[int, int]] | None = None) -> dict:
        """Analyze a 2D plate of readings (rows x cols)."""
        flat = [v for row in plate for v in row]
        blank = 0.0
        if blank_wells:
            blank = sum(plate[r][c] for r, c in blank_wells) / len(blank_wells)
        corrected = [v - blank for v in flat]
        mean = sum(corrected) / max(len(corrected), 1)
        return {"mean": round(mean, 4),
                "blank": round(blank, 4),
                "corrected_values": corrected[:20],
                "min": round(min(corrected), 4),
                "max": round(max(corrected), 4)}

    @staticmethod
    def dose_response(conc: list[float], response: list[float]) -> dict:
        """Logistic fit for dose-response (EC50)."""
        import numpy as np
        c = np.array(conc, dtype=float)
        r = np.array(response, dtype=float)
        # nonlinear fit (4-parameter logistic), simple grid/least squares
        best = None
        for ec in c:
            for hill in [1.0, 2.0, 0.5]:
                for top in [r.max(), r.min()]:
                    bot = r.min() if top == r.max() else r.max()
                    pred = bot + (top - bot) * c ** hill / (ec ** hill + c ** hill)
                    sse = float(np.sum((r - pred) ** 2))
                    if best is None or sse < best[0]:
                        best = (sse, ec, hill, top, bot)
        return {"ec50": round(best[1], 4), "hill": best[2],
                "top": round(best[3], 4), "bottom": round(best[4], 4),
                "sse": round(best[0], 4)}
