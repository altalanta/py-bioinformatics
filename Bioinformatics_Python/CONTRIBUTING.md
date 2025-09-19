# Contributing

Thanks for contributing to Bioinformatics_Python!

## Prereqs
- Python 3.10+
- Suggested: `make`, `pre-commit`

## Environment
```bash
make env
```
This sets up `.venv/` and installs dependencies from `requirements.txt`.

## Run tests
```bash
make test
```
Add tests in `tests/` for new pipelines, normalization steps, or schema tooling. Keep sample data lean.

## Code style
- Follow PEP8/black style.
- Keep reusable code under `src/pipeline/`.
- Avoid committing heavyweight outputs.

## Commit messages
- Imperative tense (`feat: add markov transition check`).
- Reference issues where helpful.

## Branching
- Branch off `main`.
- Rebase or merge as appropriate before PR.

## PR checklist
- [ ] `make test`
- [ ] `make schema-check`
- [ ] `make report-card`
- [ ] Update docs/model cards if behavior changes
- [ ] Provide or update sample configs/data as necessary
- [ ] Add/refresh tests covering new logic
