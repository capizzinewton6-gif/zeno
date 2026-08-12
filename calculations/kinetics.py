"""Kinetics — rate laws, Arrhenius equation, and reaction order."""

import math


class Kinetics:
    """Chemical kinetics calculations."""

    R = 8.314  # J/(mol*K)

    # --- Rate laws -----------------------------------------------------
    @staticmethod
    def rate_law(concentrations, rate_constant, orders):
        """rate = k * prod([C_i]^order_i)."""
        rate = rate_constant
        for c, o in zip(concentrations, orders):
            rate *= (c ** o)
        return rate

    @staticmethod
    def determine_order(conc_time_pairs):
        """Estimate reaction order from integrated rate laws (0/1/2)."""
        times = [p[0] for p in conc_time_pairs]
        concs = [p[1] for p in conc_time_pairs]
        best = None
        candidates = []
        # Zero order: [A] vs t linear
        candidates.append(("zero", concs))
        # First order: ln[A] vs t linear
        candidates.append(("first", [math.log(c) if c > 0 else float('nan') for c in concs]))
        # Second order: 1/[A] vs t linear
        candidates.append(("second", [1.0 / c if c != 0 else float('inf') for c in concs]))
        best_name = None
        best_r2 = -1
        for name, y in candidates:
            r2 = Kinetics._r_squared(times, y)
            if r2 > best_r2:
                best_r2 = r2
                best_name = name
        return {"estimated_order": best_name, "r_squared": best_r2}

    @staticmethod
    def _r_squared(x, y):
        n = len(x)
        if n < 2:
            return 0.0
        sx = sum(x); sy = sum(y)
        sxx = sum(xi * xi for xi in x)
        sxy = sum(xi * yi for xi, yi in zip(x, y))
        denom = n * sxx - sx * sx
        if denom == 0:
            return 0.0
        slope = (n * sxy - sx * sy) / denom
        intercept = (sy - slope * sx) / n
        y_mean = sy / n
        ss_res = sum((yi - (slope * xi + intercept)) ** 2 for xi, yi in zip(x, y))
        ss_tot = sum((yi - y_mean) ** 2 for yi in y)
        return 1 - ss_res / ss_tot if ss_tot != 0 else 0.0

    @staticmethod
    def half_life(order, k, initial_conc=None):
        if order == 0:
            return initial_conc / (2 * k)
        if order == 1:
            return math.log(2) / k
        if order == 2:
            return 1.0 / (k * initial_conc)
        raise ValueError("Order must be 0, 1, or 2")

    # --- Arrhenius -----------------------------------------------------
    @staticmethod
    def arrhenius_rate(A, Ea_J, T_K):
        return A * math.exp(-Ea_J / (Kinetics.R * T_K))

    @staticmethod
    def arrhenius_two_temp(k1, T1, T2, Ea_J):
        """Predict k2 from k1 using Ea."""
        return k1 * math.exp((-Ea_J / Kinetics.R) * (1.0 / T2 - 1.0 / T1))

    @staticmethod
    def activation_energy_from_rates(k1, T1, k2, T2):
        """Ea = R * ln(k2/k1) / (1/T1 - 1/T2)."""
        return Kinetics.R * math.log(k2 / k1) / (1.0 / T1 - 1.0 / T2)
