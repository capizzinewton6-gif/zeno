"""Newtonian, Lagrangian, Hamiltonian dynamics, and rigid bodies."""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
import sympy as sp


@dataclass
class State1D:
    x: float
    v: float

    def as_array(self) -> np.ndarray:
        return np.array([self.x, self.v], dtype=float)


class NewtonianDynamics:
    """Integrate Newton's second law in 1D/3D."""

    @staticmethod
    def euler(deriv: Callable, state: np.ndarray, dt: float) -> np.ndarray:
        return state + deriv(state) * dt

    @staticmethod
    def velocity_verlet(accel: Callable[[float, np.ndarray], np.ndarray], x: np.ndarray,
                        v: np.ndarray, dt: float, t: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        a0 = accel(t, x)
        x_new = x + v * dt + 0.5 * a0 * dt * dt
        a1 = accel(t + dt, x_new)
        v_new = v + 0.5 * (a0 + a1) * dt
        return x_new, v_new

    @staticmethod
    def rk4(deriv: Callable[[float, np.ndarray], np.ndarray], t: float, state: np.ndarray, dt: float) -> np.ndarray:
        k1 = deriv(t, state)
        k2 = deriv(t + dt / 2, state + k1 * dt / 2)
        k3 = deriv(t + dt / 2, state + k2 * dt / 2)
        k4 = deriv(t + dt, state + k3 * dt)
        return state + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6

    @staticmethod
    def integrate(deriv: Callable[[float, np.ndarray], np.ndarray], state0: np.ndarray,
                  t0: float, dt: float, n_steps: int, method: str = "rk4") -> np.ndarray:
        states = np.empty((n_steps + 1, *np.shape(state0)))
        states[0] = state0
        s = np.array(state0, dtype=float)
        t = t0
        for i in range(1, n_steps + 1):
            if method == "rk4":
                s = NewtonianDynamics.rk4(deriv, t, s, dt)
            elif method == "euler":
                s = NewtonianDynamics.euler(lambda st: deriv(t, st), s, dt)
            else:
                raise ValueError(f"Unknown method: {method}")
            t += dt
            states[i] = s
        return states


class LagrangianMechanics:
    """Symbolic Euler-Lagrange and Hamiltonian construction via SymPy."""

    @staticmethod
    def euler_lagrange(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Expr:
        """Compute d/dt(dL/dqdot) - dL/dq using the chain rule.

        ``q`` and ``qdot`` are treated as time-dependent functions of ``t``; the total
        time derivative of dL/dqdot is expanded via the chain rule over both q and qdot,
        which correctly produces the qddot (acceleration) term.
        """
        dL_dqdot = sp.diff(L, qdot)
        # total time derivative: d/dt(dL/dqdot) = d2_dq + d3_dqdot
        # where d2 = d(dL/dqdot)/dq and d3 = d(dL/dqdot)/dqdot, with d q/dt = qdot
        # and d qdot/dt = qddot.
        qddot = sp.Symbol(f"ddt_{qdot}")
        d_dt_dL_dqdot = sp.diff(dL_dqdot, q) * qdot + sp.diff(dL_dqdot, qdot) * qddot
        el = d_dt_dL_dqdot - sp.diff(L, q)
        return sp.simplify(el)

    @staticmethod
    def equation_of_motion(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> sp.Eq:
        return sp.Eq(LagrangianMechanics.euler_lagrange(L, q, qdot, t), 0)

    @staticmethod
    def hamiltonian_from_lagrangian(L: sp.Expr, q: sp.Symbol, qdot: sp.Symbol, t: sp.Symbol) -> tuple[sp.Symbol, sp.Expr]:
        p = sp.Symbol(f"p_{q}")
        H_expr = p * qdot - L
        # Solve L's momentum definition for qdot in terms of p
        pdef = sp.Eq(p, sp.diff(L, qdot))
        qdot_of_p = sp.solve(pdef, qdot)
        if not qdot_of_p:
            raise ValueError("Could not Legendre-transform: singular momentum definition.")
        H = sp.simplify(H_expr.subs(qdot, qdot_of_p[0]))
        return p, H


class HamiltonianMechanics:
    """Hamilton's equations and phase-space flow."""

    @staticmethod
    def equations(H: sp.Expr, q: sp.Symbol, p: sp.Symbol, t: sp.Symbol = sp.Symbol("t")) -> tuple[sp.Expr, sp.Expr]:
        qdot = sp.diff(H, p)
        pdot = -sp.diff(H, q)
        return sp.simplify(qdot), sp.simplify(pdot)


class RigidBody:
    """Moments of inertia and torque-free rigid-body rotation."""

    @staticmethod
    def inertia_tensor_solid_ellipsoid(m: float, a: float, b: float, c: float) -> np.ndarray:
        """Inertia tensor of a uniform solid ellipsoid with semi-axes a,b,c."""
        I = np.diag([
            m / 5 * (b ** 2 + c ** 2),
            m / 5 * (a ** 2 + c ** 2),
            m / 5 * (a ** 2 + b ** 2),
        ])
        return I

    @staticmethod
    def torque_free_euler(omega0: np.ndarray, I: np.ndarray, dt: float, n_steps: int) -> np.ndarray:
        """Integrate Euler's equations I1 wdot1 = (I2-I3) w2 w3 (cyclic) for a torque-free body."""
        omega = np.array(omega0, dtype=float)
        traj = np.empty((n_steps + 1, 3))
        traj[0] = omega
        for i in range(1, n_steps + 1):
            wx, wy, wz = omega
            I1, I2, I3 = np.diag(I)
            dtx = (I2 - I3) / I1 * wy * wz
            dty = (I3 - I1) / I2 * wz * wx
            dtz = (I1 - I2) / I3 * wx * wy
            omega = omega + np.array([dtx, dty, dtz]) * dt
            traj[i] = omega
        return traj


class HarmonicOscillator:
    """The canonical harmonic oscillator, analytically and on a grid."""

    def __init__(self, m: float = 1.0, k: float = 1.0):
        self.m = m
        self.k = k
        self.omega = math.sqrt(k / m)

    def solution(self, x0: float, v0: float, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        A = x0
        B = v0 / self.omega
        x = A * np.cos(self.omega * t) + B * np.sin(self.omega * t)
        v = -A * self.omega * np.sin(self.omega * t) + B * self.omega * np.cos(self.omega * t)
        return x, v

    def energy(self, x: np.ndarray, v: np.ndarray) -> np.ndarray:
        return 0.5 * self.m * v ** 2 + 0.5 * self.k * x ** 2

    def lagrangian(self):
        t, m, k = sp.symbols("t m k", positive=True)
        x = sp.Function("x")(t)
        L = sp.Rational(1, 2) * m * sp.diff(x, t) ** 2 - sp.Rational(1, 2) * k * x ** 2
        return L, (t, m, k, x)
