# Repository Guidelines

## Project Structure & Module Organization

`main.py` is the CLI entry point and wires the application together. `offers/` contains the source-independent `Offer` model, search criteria, and provider and repository protocols. `bazos_sniper/` implements the Bazoš provider: HTTP access, URL construction, pagination, parsing, and conversion of remote data into `Offer` objects belong here. Keep it independent of storage and presentation. `app/` contains CLI parsing/output, SQLite persistence, vehicle normalization, scoring, and the `SearchApplication` orchestration layer. Runtime data is written to `cars.db` and is intentionally ignored by Git.

Tests live under `tests/`; mirror the package being tested and keep saved HTML in `tests/fixtures/` when fixtures are needed.

## Development and Validation Commands

This repository has no build step or committed dependency manifest. Use the existing Windows virtual environment when available:

```powershell
.\.venv\Scripts\python.exe main.py --query bmw --limit 10
.\.venv\Scripts\python.exe -m compileall -q app bazos_sniper offers main.py tests
.\.venv\Scripts\python.exe -m pytest -v
```

The first command performs a live search and creates or updates `cars.db`; do not use it in automated tests. `compileall` provides a quick syntax check. Run `pytest` after adding or restoring tests.

## Coding Style & Naming Conventions

Follow standard Python conventions: four-space indentation, `snake_case` for modules and functions, `PascalCase` for classes, and leading underscores for internal helpers. Keep type annotations on public functions and use dataclasses for simple data objects. Prefer small, single-purpose modules and dependency injection, as demonstrated by `SearchApplication` and `BazosProvider`. No formatter or linter is configured, so match the existing import grouping and line style.

## Testing Guidelines

Use `pytest`; name files `test_<feature>.py` and tests `test_<behavior>()`. Provider, parser, pagination, and detail-enrichment tests must use local HTML fixtures or fake HTTP clients, never live Bazos requests. Cover malformed or missing fields, duplicate offers, pagination termination, database upserts, and CLI validation. No numeric coverage threshold is enforced, but every bug fix should include a regression test.

## Commit & Pull Request Guidelines

Recent commits use short, imperative, sentence-case subjects, for example `Improve Bazos listing and detail page parsing`. Keep each commit focused. Pull requests should explain the behavior change, identify affected layers, list validation commands and results, and link related issues. Include sample CLI output for user-visible changes; screenshots are only needed for future graphical interfaces.

## Security & Configuration

Never commit `.env` files, local databases, downloaded pages containing personal data, or virtual environments. Treat remote HTML as untrusted input and preserve HTTP timeouts and explicit error translation.
