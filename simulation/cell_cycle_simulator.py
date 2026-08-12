"""Cell division, signaling cascades, and apoptosis."""
from __future__ import annotations

import random


class CellCycleSimulator:
    PHASES = ["G1", "S", "G2", "M"]

    def run(self, n_cells=100, cycles=5, division_probability=0.95,
            seed=0) -> dict:
        rng = random.Random(seed)
        cells = [{"phase": "G1", "age": 0} for _ in range(n_cells)]
        phase_counts = {p: 0 for p in self.PHASES}
        history = []
        for cycle in range(cycles):
            counts = {p: 0 for p in self.PHASES}
            new_cells = []
            for cell in cells:
                idx = self.PHASES.index(cell["phase"])
                cell["phase"] = self.PHASES[(idx + 1) % len(self.PHASES)]
                cell["age"] += 1
                counts[cell["phase"]] += 1
                if cell["phase"] == "M" and rng.random() < division_probability:
                    new_cells.append({"phase": "G1", "age": 0})
                # occasional apoptosis
                if rng.random() < 0.02:
                    continue
                new_cells.append(cell)
            cells = new_cells
            history.append({"cycle": cycle, "cell_count": len(cells),
                            "phase_counts": counts.copy()})
        for p in self.PHASES:
            phase_counts[p] = sum(h["phase_counts"][p] for h in history)
        return {"initial_cells": n_cells, "cycles": cycles,
                "final_cells": len(cells), "history": history,
                "total_phase_time": phase_counts}


class ApoptosisSimulator:
    @staticmethod
    def run(stimulus_strength=0.5, threshold=0.7, cells=1000, steps=50) -> dict:
        alive = cells
        caspase = 0.0
        history = {"step": [], "alive": [], "caspase": []}
        for step in range(steps):
            caspase = min(caspase + stimulus_strength * 0.1, 1.0)
            death_rate = (caspase - threshold) if caspase > threshold else 0.0
            alive = max(int(alive - alive * death_rate * 0.2), 0)
            history["step"].append(step)
            history["alive"].append(alive)
            history["caspase"].append(round(caspase, 3))
        return {"surviving_cells": alive, "threshold": threshold, **history}
