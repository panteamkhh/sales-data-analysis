# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-09-12

### Added

- MIT `LICENSE`.
- `pyproject.toml` with project metadata, runtime/dev dependencies, and
  ruff / black / pytest configuration.
- `tests/` suite covering the loader, cleaning, feature engineering, and
  analysis functions (pytest).
- GitHub Actions CI (lint, format check, tests on Python 3.10-3.12).
- Dependabot, issue templates, and a pull request template.
- `pre-commit` hooks and `.gitattributes`.
- `CONTRIBUTING.md`, `CHANGELOG.md`, and `powerbi/dax_measures.md`.
- `src/config.py` for CWD-independent project paths and constants.
- `src/run_analysis.py` CLI to run the whole pipeline end-to-end.

### Changed

- Discount parsing now uses a regular expression and warns on unrecognized
  promotion terms instead of silently returning 0%.
- `load_data()` defaults to the bundled workbook and validates required sheets
  and columns.
- Charts annotate currency axes with INR formatting and thousands separators.
- Bottom-N products are ordered ascending so charts read naturally.
- README rewritten with badges, table of contents, dataset notes, and
  cross-platform setup instructions.

### Fixed

- `compare_periods` no longer produces infinite percent change when the base
  period has zero activity.
- `filter_orders` correctly handles falsy filter values such as customer id `0`.
- Corrected optional type hints in `analysis.filter_orders`.
