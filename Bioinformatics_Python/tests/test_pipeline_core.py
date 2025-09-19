from pathlib import Path

import numpy as np
import pandas as pd

from src.pipeline.cluster import cluster_embed
from src.pipeline.normalization import log1p_guarded
from src.pipeline.transitions import make_markov


def test_log1p_guarded_idempotent():
    df = pd.DataFrame([[0, 1], [2, 3]], columns=["a", "b"])
    norm1 = log1p_guarded(df)
    norm2 = log1p_guarded(norm1)
    assert np.allclose(norm1.values, norm2.values)


def test_cluster_seed_stability():
    emb = np.random.RandomState(0).randn(50, 5)
    out1 = cluster_embed(emb, seed=0)
    out2 = cluster_embed(emb, seed=0)
    assert out1["n_clusters"] == out2["n_clusters"]
    assert np.array_equal(out1["labels"], out2["labels"])


def test_markov_rows_sum_to_one():
    counts = np.array([[1, 3, 6], [0, 5, 5]])
    tm = make_markov(counts)
    assert np.allclose(tm.sum(axis=1), 1.0, atol=1e-6)
    assert (tm >= 0).all()


def test_schema_check(tmp_path, monkeypatch):
    from tools import schema_check

    config = tmp_path / "config.json"
    config.write_text((Path("configs/input.json")).read_text(), encoding="utf-8")

    exit_code = schema_check.validate_config(config)
    assert exit_code == 0
