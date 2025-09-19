"""Render analysis card for RNA-seq workflows."""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

DEFAULT_CARD = Path("reports/analysis_card.md")
DEFAULT_CONFIG = Path("configs/input.json")
DEFAULT_METRICS = Path("reports/metrics.json")

TEMPLATE = """# Analysis Card: Bioinformatics_Python

- Generated: {timestamp}
- Commit: `{commit}`
- Config: `{config}`

## Use Case
State/transition exploration for small RNA-seq cohorts; **not** for diagnostics.

## Data
- Expression matrix: `{matrix}`
- Feature axis: `{feature_axis}`
- Normalization: `{normalization}`
- Samples: {n_samples}

## Methods
- Normalization: log1p guard to prevent double-application.
- Embedding/clustering: KMeans on latent embedding.
- Transition estimation: row-normalized Markov matrix.

## Quality Checks
- Log normalization idempotence test
- Batch column handled in pipeline interface
- Cluster stability (seeded)
- Transition matrix rows sum to 1

## Metrics / Notes
{metrics_block}

## Assumptions & Limitations
- Synthetic toy dataset; update with real QCed counts before production use.
- Sensitive to normalization choice and sparsity.
- Batch correction hooks provided but not applied by default.

## Outputs
- Cluster labels, Markov transitions, exploratory figures (if generated externally).

## Versioning
- Metrics path: `{metrics_path}`
"""


def git_sha() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
            .decode()
            .strip()
        )
    except Exception:
        return "unknown"


def load_metrics(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Render analysis card")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="Config JSON path")
    parser.add_argument("--metrics", default=str(DEFAULT_METRICS), help="Metrics JSON path (optional)")
    parser.add_argument("--out", default=str(DEFAULT_CARD), help="Output markdown path")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = json.loads(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
    matrix = config.get("X_path", "n/a")
    feature_axis = config.get("feature_axis", "n/a")
    normalization = config.get("normalization", "n/a")
    samples = len(config.get("sample_meta", []))

    metrics = load_metrics(Path(args.metrics))
    if metrics:
        metrics_block = "\n".join(f"- **{k}**: {v}" for k, v in metrics.items())
    else:
        metrics_block = "Metrics not available. Run your pipeline and dump JSON to reports/metrics.json."

    content = TEMPLATE.format(
        timestamp=datetime.utcnow().isoformat() + "Z",
        commit=git_sha(),
        config=args.config,
        matrix=matrix,
        feature_axis=feature_axis,
        normalization=normalization,
        n_samples=samples,
        metrics_block=metrics_block,
        metrics_path=args.metrics,
    )

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    print(f"Analysis card written to {out_path}")


if __name__ == "__main__":  # pragma: no cover
    main()
