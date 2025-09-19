# Analysis Card: Bioinformatics_Python

- Generated: 2025-09-19T19:18:49.969112Z
- Commit: `60694b1`
- Config: `configs/input.json`

## Use Case
State/transition exploration for small RNA-seq cohorts; **not** for diagnostics.

## Data
- Expression matrix: `data/expression_matrix.csv`
- Feature axis: `genes_rows`
- Normalization: `log1p`
- Samples: 5

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
Metrics not available. Run your pipeline and dump JSON to reports/metrics.json.

## Assumptions & Limitations
- Synthetic toy dataset; update with real QCed counts before production use.
- Sensitive to normalization choice and sparsity.
- Batch correction hooks provided but not applied by default.

## Outputs
- Cluster labels, Markov transitions, exploratory figures (if generated externally).

## Versioning
- Metrics path: `reports/metrics.json`
