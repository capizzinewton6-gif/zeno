"""Molecular dynamics of biological macromolecules (simple Langevin)."""
from __future__ import annotations

import math
import random


class ProteinDynamics:
    """A toy Langevin dynamics integrator for a harmonic polymer.

    This is a pedagogical 1D bead-spring model, NOT a full force field. It
    demonstrates MD concepts (potential/kinetic energy, temperature coupling)
    without requiring OpenMM.
    """

    def run(self, n_beads=10, n_steps=1000, temperature=300,
             dt=0.002, bond_k=100.0, seed=0) -> dict:
        rng = random.Random(seed)
        # initialize positions around 0
        positions = [i * 1.0 for i in range(n_beads)]
        velocities = [rng.gauss(0, math.sqrt(temperature / 300.0)) for _ in range(n_beads)]
        energies = []
        for step in range(n_steps):
            forces = [0.0] * n_beads
            # harmonic bond forces between adjacent beads (equilibrium length 1.0)
            for i in range(n_beads - 1):
                dx = positions[i + 1] - positions[i] - 1.0
                f = -bond_k * dx
                forces[i] += f
                forces[i + 1] -= f
            # Langevin thermostat
            gamma = 1.0
            for i in range(n_beads):
                noise = rng.gauss(0, math.sqrt(2 * gamma * temperature / 300.0))
                velocities[i] += (forces[i] - gamma * velocities[i]) * dt + noise * math.sqrt(dt)
                positions[i] += velocities[i] * dt
            if step % max(n_steps // 50, 1) == 0:
                ke = 0.5 * sum(v * v for v in velocities)
                pe = 0.0
                for i in range(n_beads - 1):
                    dx = positions[i + 1] - positions[i] - 1.0
                    pe += 0.5 * bond_k * dx * dx
                energies.append({"step": step, "KE": round(ke, 4),
                                 "PE": round(pe, 4), "total": round(ke + pe, 4)})
        return {"n_beads": n_beads, "steps": n_steps, "temperature": temperature,
                "energy_trace": energies[-10:], "final_positions": [round(p, 3) for p in positions]}
