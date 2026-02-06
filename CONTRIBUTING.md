# Contributing

## Workflow

1. Fork and create a feature branch.
2. Keep changes focused (single concern per PR).
3. Update docs when behavior or configuration changes.

## Local setup

```bash
uv sync --dev
cp .env.example .env
```

Fill required `DB_*` variables in `.env`.

## Required checks before PR

```bash
uv run ruff check .
uv run pyright
uv run verify <exchange_id>
```

For exchange adapter changes, `verify` is the primary validation gate.

Useful commands:

```bash
uv run verify --list
uv run verify hyperliquid --history-days 7
```

## Exchange adapter changes

1. Start from `funding_tracker/exchanges/_template.py`.
2. Register adapter in `funding_tracker/exchanges/__init__.py`.
3. Run `uv run verify <exchange_id>` and include result summary in PR description.
