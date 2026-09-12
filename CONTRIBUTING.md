# Contributing

Thanks for your interest in improving this project. This document describes the
local workflow and expectations.

## Development setup

```bash
git clone https://github.com/panteamkhh/sales-data-analysis.git
cd sales-data-analysis
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev]"
pre-commit install
```

## Running the analysis

```bash
python -m src.run_analysis
```

This regenerates every chart in `screenshots/` and writes
`output/master_sales_data.csv`. The notebook in `notebooks/` runs the same
pipeline interactively.

## Quality gates

Before opening a pull request, make sure these pass:

```bash
ruff check .
black --check .
pytest
```

`pre-commit run --all-files` runs the same checks plus whitespace/file hygiene.

## Commit messages

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add monthly seasonality breakdown
fix: handle empty base period in compare_periods
docs: clarify profit margin assumption
test: cover discount parser edge cases
chore: bump pandas
```

## Pull requests

- Keep changes focused; one logical change per PR.
- Add or update tests for behaviour changes.
- Update the README / CHANGELOG when user-facing behaviour changes.
- Never commit secrets, credentials, or real personal data.
