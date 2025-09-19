"""Normalization utilities with idempotence guards."""

from __future__ import annotations

import numpy as np
import pandas as pd


def log1p_guarded(matrix: pd.DataFrame) -> pd.DataFrame:
    """Apply log1p exactly once, tagging the DataFrame to prevent double-log."""
    if matrix.attrs.get("log1p_applied"):
        return matrix.copy()
    transformed = np.log1p(matrix)
    if isinstance(transformed, np.ndarray):
        transformed = pd.DataFrame(transformed, index=getattr(matrix, "index", None), columns=getattr(matrix, "columns", None))
    transformed.attrs["log1p_applied"] = True
    return transformed
