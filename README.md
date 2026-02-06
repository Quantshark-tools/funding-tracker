# Funding Tracker

Collects funding rates from crypto exchanges for perpetual contracts.

## Quick Start

```bash
docker-compose up
```

## Environment Variables

- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DBNAME`: PostgreSQL connection settings
- `FT_ENGINE_KWARGS`: JSON object with funding-tracker engine kwargs (optional)
- `FT_SESSION_KWARGS`: JSON object with funding-tracker session kwargs (optional)
- `EXCHANGES`: Comma-separated list of exchanges to run (default: all)
- `DEBUG_EXCHANGES`: Comma-separated list for DEBUG logging (independent of execution)

## Local Development

### Run with specific exchanges

```bash
# Run all exchanges
funding-tracker

# Run single exchange
funding-tracker --exchanges hyperliquid

# Run multiple exchanges
funding-tracker --exchanges hyperliquid,bybit

# Via environment variable
EXCHANGES=hyperliquid,bybit funding-tracker

# CLI overrides environment variable
EXCHANGES=bybit funding-tracker --exchanges hyperliquid  # Runs hyperliquid only
```

### Debug logging

```bash
# Enable debug logging for specific exchanges (independent of execution)
funding-tracker --exchanges hyperliquid --debug-exchanges hyperliquid,bybit

# Via environment variable
DEBUG_EXCHANGES=hyperliquid,bybit funding-tracker
```

### Verify exchange adapter

```bash
uv run verify <exchange_id>

# Example
uv run verify hyperliquid
```

## Docker Deployment

See [deploy/README.md](deploy/README.md) for Docker deployment instructions.

## Adding New Exchanges

See `funding_tracker/exchanges/_template.py` for implementation guide.

## Architecture

- **Exchanges**: Protocol-based adapters for each exchange API
- **Coordinators**: Business logic for syncing contracts, fetching history, collecting live rates
- **Scheduler**: APScheduler-based job orchestration with even distribution
- **Database**: TimescaleDB with hypertables for time-series data

## License

MIT
