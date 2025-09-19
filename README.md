# Bioinformatics_Python


Synthetic RNA-seq analysis toolbox demonstrating normalization, clustering, and transition modeling.

## Quickstart
```bash
make env
pytest -q
python -m tools.schema_check --config configs/input.json
python -m tools.render_card --config configs/input.json
```

- Schema: [`schema/rnaseq_matrix.schema.json`](schema/rnaseq_matrix.schema.json)
- Analysis card: [`reports/analysis_card.md`](reports/analysis_card.md)

## Contents
- `data/` tiny toy dataset + metadata
- `configs/input.json` example config for schema validation & renders
- `src/pipeline/` reusable modules
- `tools/` schema validation and analysis-card rendering helpers
- `tests/` unit tests for core normalization/clustering/transition logic

Generate the analysis card with:`make report-card` after running pipelines.
