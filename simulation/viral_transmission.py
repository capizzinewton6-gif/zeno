"""SIR and epidemiological infection models."""
from __future__ import annotations


class SIRModel:
    def run(self, population=10000, i0=1, beta=0.3, gamma=0.1, days=160) -> dict:
        s, i, r = float(population - i0), float(i0), 0.0
        history = {"day": [], "S": [], "I": [], "R": []}
        for day in range(days):
            new_inf = beta * s * i / population
            new_rec = gamma * i
            s = max(s - new_inf, 0.0)
            i = max(i + new_inf - new_rec, 0.0)
            r = max(r + new_rec, 0.0)
            history["day"].append(day)
            history["S"].append(round(s, 1))
            history["I"].append(round(i, 1))
            history["R"].append(round(r, 1))
        r0 = round(beta / gamma, 3)
        peak_i = round(max(history["I"]), 1)
        peak_day = history["I"].index(max(history["I"]))
        return {"params": dict(population=population, i0=i0, beta=beta, gamma=gamma, days=days),
                "r0": r0, "peak_infected": peak_i, "peak_day": peak_day, **history}


class SEIRModel:
    def run(self, population=10000, e0=1, beta=0.3, sigma=0.2, gamma=0.1, days=160) -> dict:
        s, e, i, r = float(population - e0), float(e0), 0.0, 0.0
        history = {"day": [], "S": [], "E": [], "I": [], "R": []}
        for day in range(days):
            new_exp = beta * s * i / population
            new_inf = sigma * e
            new_rec = gamma * i
            s -= new_exp
            e += new_exp - new_inf
            i += new_inf - new_rec
            r += new_rec
            history["day"].append(day)
            history["S"].append(round(s, 1))
            history["E"].append(round(e, 1))
            history["I"].append(round(i, 1))
            history["R"].append(round(r, 1))
        return {"r0": round(beta / gamma, 3), **history}
