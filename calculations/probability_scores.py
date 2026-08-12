"""Probability scores: softmax, sigmoid, Bayesian confidence."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def softmax(logits: Sequence[float]) -> np.ndarray:
    x = np.asarray(logits, dtype=np.float64)
    x = x - np.max(x)
    e = np.exp(x)
    return (e / np.sum(e)).astype(np.float32)


def sigmoid(x: float) -> float:
    return float(1.0 / (1.0 + np.exp(-x)))


def sigmoid_array(x: Sequence[float]) -> np.ndarray:
    arr = np.asarray(x, dtype=np.float64)
    return (1.0 / (1.0 + np.exp(-arr))).astype(np.float32)


def bayesian_update(prior: float, likelihood: float, evidence: float) -> float:
    """Posterior = (likelihood * prior) / evidence, all in [0, 1]."""
    if evidence <= 0:
        return prior
    return float((likelihood * prior) / evidence)


def confidence_threshold(score: float, threshold: float = 0.5) -> bool:
    return score >= threshold


def entropy(probs: Sequence[float]) -> float:
    p = np.asarray(probs, dtype=np.float64)
    p = np.clip(p, 1e-12, 1.0)
    return float(-np.sum(p * np.log(p)))
