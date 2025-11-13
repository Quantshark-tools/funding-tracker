# Funding Tracker

Collects funding rates from crypto exchanges for perpetual contracts.

## Quick Start

```bash
docker-compose up
```

## Environment Variables

- `DB_CONNECTION`: PostgreSQL connection string (required)

## Adding New Exchanges

See `funding_tracker/exchanges/_template.py` for implementation guide.

## Architecture

- **Exchanges**: Protocol-based adapters for each exchange API
- **Coordinators**: Business logic for syncing contracts, fetching history, collecting live rates
- **Scheduler**: APScheduler-based job orchestration with even distribution
- **Database**: TimescaleDB with hypertables for time-series data

## License

MIT
