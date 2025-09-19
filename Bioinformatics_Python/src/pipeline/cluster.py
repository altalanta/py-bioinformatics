"""Clustering helpers."""

from __future__ import annotations

from typing import Dict

import numpy as np
from sklearn.cluster import KMeans


def cluster_embed(embedding: np.ndarray, seed: int = 0, n_clusters: int | None = None) -> Dict[str, object]:
    if n_clusters is None:
        n_clusters = max(2, min(6, embedding.shape[0] // 20 or 2))
    model = KMeans(n_clusters=n_clusters, random_state=seed, n_init=10)
    labels = model.fit_predict(embedding)
    return {"labels": labels, "n_clusters": int(n_clusters)}
