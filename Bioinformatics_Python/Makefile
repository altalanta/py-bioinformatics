.PHONY: env test lint schema-check report-card

env:
	python -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

test:
	. .venv/bin/activate || true; pytest -q

lint:
	echo "Add lint tooling as needed."

schema-check:
	python -m tools.schema_check --config configs/input.json

report-card:
	python -m tools.render_card --config configs/input.json
