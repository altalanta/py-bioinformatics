"""Validate RNA-seq config against schema and data dimensions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from jsonschema import Draft7Validator

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema" / "rnaseq_matrix.schema.json"


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def validate_config(config_path: Path) -> int:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    schema = load_schema()
    validator = Draft7Validator(schema)
    errors = list(validator.iter_errors(config))
    if errors:
        print(f"Schema violations in {config_path}:")
        for err in errors[:5]:
            print(f" - {err.message}")
        return 1

    matrix_path = config_path.parent / config["X_path"] if not Path(config["X_path"]).is_absolute() else Path(config["X_path"])
    if not matrix_path.exists():
        print(f"Matrix file not found: {matrix_path}")
        return 1
    df = pd.read_csv(matrix_path)
    sample_meta = config["sample_meta"]
    sample_ids = [row["sample_id"] for row in sample_meta]

    if config["feature_axis"] == "genes_rows":
        columns = list(df.columns)[1:]
    else:
        columns = list(df.iloc[:, 0])
    if columns != sample_ids:
        print("Sample IDs mismatch between matrix and metadata")
        return 1
    print(f"Schema check passed for {config_path} (matrix: {matrix_path})")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate RNA-seq config and matrix")
    parser.add_argument("--config", default="configs/input.json", help="Path to config JSON")
    args = parser.parse_args()
    exit(validate_config(Path(args.config)))


if __name__ == "__main__":  # pragma: no cover
    main()
