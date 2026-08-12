"""Multi-well plate layouts (96-well, 384-well)."""
from __future__ import annotations


class CellCultureLayout:
    ROWS_96 = 8   # A-H
    COLS_96 = 12

    ROWS_384 = 16
    COLS_384 = 24

    @staticmethod
    def generate_plate(format: str = "96") -> list[str]:
        if format == "96":
            rows, cols = 8, 12
        elif format == "384":
            rows, cols = 16, 24
        elif format == "6":
            rows, cols = 2, 3
        elif format == "24":
            rows, cols = 4, 6
        else:
            rows, cols = 8, 12
        wells = []
        for r in range(rows):
            for c in range(1, cols + 1):
                wells.append(f"{chr(65 + r)}{c}")
        return wells

    @staticmethod
    def layout_samples(samples: list[str], format: str = "96",
                       replicates: int = 3, controls: dict | None = None) -> dict:
        wells = CellCultureLayout.generate_plate(format)
        layout = {}
        idx = 0
        for s in samples:
            for rep in range(replicates):
                if idx < len(wells):
                    layout[wells[idx]] = f"{s}_r{rep + 1}"
                    idx += 1
        if controls:
            for well, ctrl in controls.items():
                layout[well] = ctrl
        return {"format": format, "layout": layout,
                "wells_used": len(layout), "total_wells": len(wells)}

    @staticmethod
    def edge_effect_zones(format: str = "96") -> dict:
        wells = CellCultureLayout.generate_plate(format)
        return {"edge_wells": [w for w in wells if w[0] in "AH" or int(w[1:]) in (1, 12)],
                "center_wells": [w for w in wells if w[0] not in "AH" and int(w[1:]) not in (1, 12)]}
