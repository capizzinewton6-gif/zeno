"""Time-step integrators: Verlet, RK4, RK45, Leapfrog, Euler."""

from __future__ import annotations

from typing import Callable

import numpy as np


class Integrators:
    """Reusable ODE integrators shared by all simulators."""

    @staticmethod
    def euler(deriv: Callable, state: np.ndarray, dt: float, t: float = 0.0) -> np.ndarray:
        return state + deriv(t, state) * dt

    @staticmethod
    def leapfrog(accel: Callable[[float, np.ndarray], np.ndarray], x: np.ndarray, v: np.ndarray,
                 dt: float, t: float = 0.0) -> tuple[np.ndarray, np.ndarray]:
        v_half = v + 0.5 * accel(t, x) * dt
        x_new = x + v_half * dt
        a_new = accel(t + dt, x_new)
        v_new = v_half + 0.5 * a_new * dt
        return x_new, v_new

    @staticmethod
    def verlet(accel: Callable[[float, np.ndarray], np.ndarray], x: np.ndarray, x_prev: np.ndarray,
               dt: float, t: float = 0.0) -> np.ndarray:
        """Position Verlet (Stormer) step: x_{n+1} = 2 x_n - x_{n-1} + a dt^2."""
        return 2 * x - x_prev + accel(t, x) * dt ** 2

    @staticmethod
    def rk4(deriv: Callable[[float, np.ndarray], np.ndarray], t: float, state: np.ndarray, dt: float) -> np.ndarray:
        k1 = deriv(t, state)
        k2 = deriv(t + dt / 2, state + k1 * dt / 2)
        k3 = deriv(t + dt / 2, state + k2 * dt / 2)
        k4 = deriv(t + dt, state + k3 * dt)
        return state + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6

    @staticmethod
    def rk45_step(deriv, t: float, state: np.ndarray, dt: float, atol: float = 1e-9):
        """Adaptive Dormand-Prince (RK45) via scipy fallback."""
        from scipy.integrate import solve_ivp
        sol = solve_ivp(deriv, [t, t + dt], state, rtol=atol, atol=atol, dense_output=False, method="RK45")
        return sol.y[:, -1]

    @staticmethod
    def integrate(deriv: Callable, state0: np.ndarray, dt: float, n_steps: int,
                  method: str = "rk4", t0: float = 0.0) -> np.ndarray:
        states = np.empty((n_steps + 1, *np.shape(state0)))
        states[0] = state0
        s = np.array(state0, dtype=float)
        t = t0
        for i in range(1, n_steps + 1):
            if method == "rk4":
                s = Integrators.rk4(deriv, t, s, dt)
            elif method == "euler":
                s = Integrators.euler(deriv, s, dt, t)
            elif method == "leapfrog":
                # requires (x, v) layout
                half = len(s) // 2
                x, v = s[:half], s[half:]
                x, v = Integrators.leapfrog(lambda tt, xx: deriv(tt, np.concatenate([xx, v]))[:half], x, v, dt, t)
                s = np.concatenate([x, v])
            else:
                raise ValueError(f"Unknown integrator: {method}")
            t += dt
            states[i] = s
        return states


INTEGRATORS = Integrators()
