"""Grid-based discrete systems and Wolfram rule generators."""

from __future__ import annotations

from typing import Any

import numpy as np


def rule_number_to_rule(rule: int) -> dict[int, int]:
    """Convert a Wolfram elementary CA rule number (0-255) to a lookup table."""
    table = {}
    for i in range(8):
        table[i] = (rule >> i) & 1
    return table


def evolve(rule: int, initial: list[int], steps: int) -> list[list[int]]:
    """Evolve a 1-D elementary cellular automaton for ``steps``."""
    lookup = rule_number_to_rule(rule)
    n = len(initial)
    state = list(initial)
    history = [list(state)]
    for _ in range(steps):
        new = []
        for i in range(n):
            pattern = 4 * state[(i - 1) % n] + 2 * state[i] + state[(i + 1) % n]
            new.append(lookup[pattern])
        state = new
        history.append(list(state))
    return history


def random_initial(size: int, p: float = 0.5, seed: int | None = None) -> list[int]:
    rng = np.random.default_rng(seed)
    return (rng.random(size) < p).astype(int).tolist()


def single_seed(size: int) -> list[int]:
    state = [0] * size
    state[size // 2] = 1
    return state


def totalistic_rule(code: int, k: int = 2, r: int = 1) -> dict[int, int]:
    """A totalistic CA rule: based on the sum of the neighbourhood."""
    table = {}
    states = k ** (2 * r + 1)
    for s in range(states):
        table[s] = (code // (k ** s)) % k
    return table


def conway_game_of_life(grid: list[list[int]], steps: int) -> list[list[list[int]]]:
    """Conway's Game of Life for ``steps`` generations with zero boundary."""
    g = np.array(grid, dtype=int)
    history = [g.tolist()]
    for _ in range(steps):
        neighbor_sum = sum(np.roll(np.roll(g, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1)) - g
        g = ((g == 1) & ((neighbor_sum == 2) | (neighbor_sum == 3))) | ((g == 0) & (neighbor_sum == 3))
        g = g.astype(int)
        history.append(g.tolist())
    return history


def wolfram_rules_list() -> list[int]:
    """Return some notable elementary CA rules."""
    return [30, 54, 60, 62, 90, 102, 110, 126, 150, 158, 188, 190, 220, 222, 250]


__all__ = [
    "rule_number_to_rule", "evolve", "random_initial", "single_seed",
    "totalistic_rule", "conway_game_of_life", "wolfram_rules_list",
]
