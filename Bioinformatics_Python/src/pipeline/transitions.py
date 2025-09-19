"""Transition matrix utilities."""

from __future__ import annotations

import numpy as np


def make_markov(counts: np.ndarray, epsilon: float = 1e-12) -> np.ndarray:
    counts = np.asarray(counts, dtype=float)
    row_sums = counts.sum(axis=1, keepdims=True)
    safe = np.where(row_sums > 0, row_sums, epsilon)
    matrix = counts / safe
    # ensure no negative values after division
    matrix[matrix < 0] = 0
    return matrix
