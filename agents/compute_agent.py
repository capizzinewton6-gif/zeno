"""Executes numerical integration, PDE solving, and field calculations.

This is the bridge between the user interface and the simulation + calculation
modules. ``run_simulation`` is the single entry point the UI calls to produce
frames that are rendered live.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Callable

import numpy as np

from physics.classical_mechanics import HarmonicOscillator
from physics.quantum_mechanics import InfiniteSquareWell, HarmonicOscillatorQuantum
from simulation.simulation_manager import Integrators
from simulation.particle_simulator import NBodySimulator, NBodyConfig
from simulation.monte_carlo_physics import IsingMonteCarlo
from simulation.continuum_fluid_sim import NavierStokes2D
from simulation.wave_optics_simulator import FDTD1D, FDTD2D
from simulation.quantum_circuit_sim import QuantumCircuitSim
from simulation.relativity_geodesic_sim import RelativityGeodesicSim
from tools.constant_engine import CONSTANTS


@dataclass
class SimulationResult:
    name: str
    frames: Any  # array of states for animation
    metadata: dict
    plotter: Callable | None = None  # function(frames, ax) for UI rendering


class ComputeAgent:
    """Dispatches numerical computations and simulations."""

    def run_simulation(self, name: str, **params) -> SimulationResult:
        method = getattr(self, f"sim_{name}", None)
        if method is None:
            raise ValueError(f"Unknown simulation: {name}. Available: "
                             f"{[m[4:] for m in dir(self) if m.startswith('sim_')]}")
        return method(**params)

    # ---- simulation catalog -------------------------------------------------

    def sim_harmonic_oscillator(self, m: float = 1.0, k: float = 1.0, x0: float = 1.0,
                                v0: float = 0.0, t_final: float = 10.0, n_steps: int = 1000) -> SimulationResult:
        ho = HarmonicOscillator(m, k)
        deriv = lambda t, s: np.array([s[1], -ho.omega ** 2 * s[0]])
        state0 = np.array([x0, v0])
        dt = t_final / n_steps
        traj = Integrators.integrate(deriv, state0, dt, n_steps, method="rk4")
        t = np.linspace(0, t_final, n_steps + 1)
        return SimulationResult("harmonic_oscillator", np.vstack([t, traj[:, 0], traj[:, 1]]).T,
                                {"omega": ho.omega, "m": m, "k": k},
                                plotter=self._plot_oscillator)

    @staticmethod
    def _plot_oscillator(frames, ax):
        data = frames if not isinstance(frames, list) else frames
        t, x, v = data[:, 0], data[:, 1], data[:, 2]
        ax.plot(t, x, label="x(t)")
        ax.plot(t, v, label="v(t)")
        ax.set_xlabel("t")
        ax.set_ylabel("x, v")
        ax.set_title("Harmonic Oscillator")
        ax.legend()

    def sim_quantum_well(self, n: int = 2, L: float = 1.0, nx: int = 300) -> SimulationResult:
        well = InfiniteSquareWell(L=L)
        x = np.linspace(0, L, nx)
        prob = well.probability_density(n, x)
        return SimulationResult("quantum_well", np.vstack([x, prob]).T,
                                {"n": n, "L": L, "E_n": well.energy(n)},
                                plotter=self._plot_well)

    @staticmethod
    def _plot_well(frames, ax):
        x, prob = frames[:, 0], frames[:, 1]
        ax.plot(x, prob, color="#e69f00")
        ax.set_xlabel("x")
        ax.set_ylabel("|psi|^2")
        ax.set_title("Infinite Square Well probability density")

    def sim_qho(self, n: int = 0, m=None, omega: float = 1.0, nx: int = 400, x_max: float = 8.0) -> SimulationResult:
        # Work in natural units (hbar=1) for visualization unless explicitly overridden.
        # With hbar=1 and m=omega=1 the oscillator length is 1, so the wavefunction is
        # visible on a macroscopic grid. The energy is reported in natural units.
        import physics.quantum_mechanics as qm
        m = m if m is not None else 1.0
        # temporarily use hbar=1 for visualization
        orig_hbar = qm.HBAR
        qm.HBAR = 1.0
        try:
            qho = HarmonicOscillatorQuantum(m=m, omega=omega)
            x = np.linspace(-x_max, x_max, nx)
            prob = qho.probability_density(n, x)
            meta = {"n": n, "E_n (natural units)": qho.energy(n), "units": "hbar=m=omega=1"}
        finally:
            qm.HBAR = orig_hbar
        return SimulationResult("quantum_harmonic_oscillator", np.vstack([x, prob]).T,
                                meta,
                                plotter=ComputeAgent._plot_qho)

    @staticmethod
    def _plot_qho(frames, ax):
        x, prob = frames[:, 0], frames[:, 1]
        ax.plot(x, prob, color="#56b4e9")
        ax.set_xlabel("x")
        ax.set_ylabel("|psi|^2")
        ax.set_title("Quantum Harmonic Oscillator")

    def sim_nbody(self, n_bodies: int = 3, t_final: float = 2.0, n_steps: int = 600) -> SimulationResult:
        rng = np.random.default_rng(42)
        pos = rng.uniform(-1, 1, (n_bodies, 3))
        vel = rng.uniform(-0.3, 0.3, (n_bodies, 3))
        masses = np.ones(n_bodies)
        sim = NBodySimulator(NBodyConfig(pos, vel, masses), softening=0.1)
        dt = t_final / n_steps
        hist = sim.run(dt, n_steps, record_every=5)
        return SimulationResult("n_body", hist, {"n_bodies": n_bodies, "dt": dt},
                                plotter=self._plot_nbody)

    @staticmethod
    def _plot_nbody(frames, ax):
        traj = frames
        for i in range(traj.shape[1]):
            ax.plot(traj[:, i, 0], traj[:, i, 1])
        ax.set_title("N-body gravitational dynamics")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_aspect("equal")

    def sim_ising(self, n: int = 32, T: float = 2.27, n_steps: int = 50) -> SimulationResult:
        sim = IsingMonteCarlo(n=n, T=T)
        result = sim.run(n_steps)
        frames = np.array(result["energy_history"]) if result["energy_history"] else np.zeros(1)
        return SimulationResult("ising", sim.lattice,
                                {"T": T, "final_energy": result["final_energy"], "mag": result["final_mag"]},
                                plotter=self._plot_ising)

    @staticmethod
    def _plot_ising(frames, ax):
        ax.imshow(frames, cmap="RdBu", vmin=-1, vmax=1, origin="lower")
        ax.set_title("2D Ising model configuration")

    def sim_fdtd(self, n_steps: int = 400, record_every: int = 8) -> SimulationResult:
        fdtd = FDTD1D(nx=200)
        hist = fdtd.run(n_steps, record_every=record_every)
        return SimulationResult("fdtd_1d", hist, {"dt": fdtd.dt, "dx": fdtd.dx},
                                plotter=self._plot_fdtd)

    @staticmethod
    def _plot_fdtd(frames, ax):
        last = frames[-1]
        ax.plot(last, color="#009e73")
        ax.set_xlabel("grid index")
        ax.set_ylabel("E_z")
        ax.set_title("FDTD electromagnetic wave (1D)")

    def sim_geodesic(self, b: float = 5.5, n_steps: int = 1500) -> SimulationResult:
        sim = RelativityGeodesicSim(rs=1.0)
        traj = sim.photon_orbit(b=b, n_steps=n_steps)
        xy = sim.to_xy(traj)
        return SimulationResult("blackhole_geodesic", xy,
                                {"impact_parameter": b, "rs": 1.0},
                                plotter=self._plot_geodesic)

    @staticmethod
    def _plot_geodesic(frames, ax):
        ax.plot(frames[:, 0], frames[:, 1], color="#cc79a7")
        theta = np.linspace(0, 2 * math.pi, 200)
        ax.plot(np.cos(theta), np.sin(theta), color="black", linewidth=2, label="event horizon")
        ax.set_aspect("equal")
        ax.set_title("Photon geodesic near Schwarzschild black hole")
        ax.legend()

    def sim_navier_stokes(self, n_steps: int = 200, record_every: int = 10) -> SimulationResult:
        ns = NavierStokes2D(n=48, nu=1e-3)
        frames = ns.run(dt=0.01, n_steps=n_steps, record_every=record_every)
        return SimulationResult("navier_stokes", frames, {"nu": ns.nu, "grid": ns.n},
                                plotter=self._plot_ns)

    @staticmethod
    def _plot_ns(frames, ax):
        ax.imshow(frames[-1], cmap="RdBu", origin="lower", aspect="auto")
        ax.set_title("2D Navier-Stokes vorticity")
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    def sim_quantum_circuit(self, gates: list[str] | None = None, shots: int = 1000) -> SimulationResult:
        qc = QuantumCircuitSim(n_qubits=2)
        qc.apply_gate(QuantumCircuitSim.H, 0)
        qc.apply_cnot(0, 1)
        counts = qc.measure(shots=shots)
        return SimulationResult("bell_state", counts, {"n_qubits": 2, "state_dim": len(qc.state)},
                                plotter=self._plot_bell)

    @staticmethod
    def _plot_bell(frames, ax):
        counts = frames
        states = list(counts.keys())
        vals = list(counts.values())
        ax.bar(states, vals, color="#0072b2")
        ax.set_ylabel("counts")
        ax.set_title("Bell-state measurement")
