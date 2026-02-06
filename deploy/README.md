# Docker Deployment

## Prerequisites

- Docker
- Docker Compose

## Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

### Environment Variables

- `DB_CONNECTION`: PostgreSQL connection string (required)
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_DBNAME`: database settings for `db-migrate` (should match `DB_CONNECTION`)
- `EXCHANGES`: Comma-separated list of exchanges to run (default: all, empty = run all)
- `DEBUG_EXCHANGES`: Comma-separated list for DEBUG logging (independent of execution)

### Multi-Instance Configuration

The application supports horizontal scaling by splitting exchanges across multiple worker instances.

- `INSTANCE_COUNT`: Number of worker instances (default: 3)
  - Exchanges are distributed evenly using round-robin
  - Each instance runs independently with autorestart
  - All instances log to stdout/stderr

Examples:

```bash
# Run with 1 instance (all exchanges on single worker)
INSTANCE_COUNT=1 docker-compose up

# Run with 3 instances (default)
docker-compose up

# Run with 5 instances
INSTANCE_COUNT=5 docker-compose up

# Check supervisord status
docker exec funding-tracker-app supervisorctl status
```

## Running

### Start all services

```bash
docker-compose up
```

This starts:
- `timescaledb`
- `db-migrate` (runs shared migrations and exits)
- `funding-tracker` (starts only after successful migrations)

### Start with specific exchanges

```bash
# Via .env file (add: EXCHANGES=hyperliquid,bybit)
docker-compose up

# Via environment variable before command
EXCHANGES=hyperliquid,bybit docker-compose up

# Single exchange
EXCHANGES=hyperliquid docker-compose up
```

### Enable debug logging

```bash
# Via .env file (add: DEBUG_EXCHANGES=hyperliquid,bybit)
docker-compose up

# Via environment variable before command
DEBUG_EXCHANGES=hyperliquid,bybit docker-compose up
```

### Combine options

```bash
EXCHANGES=hyperliquid DEBUG_EXCHANGES=hyperliquid,bybit docker-compose up
```

## Local Development

### Connect to local database

Create `docker-compose.override.yaml` to expose PostgreSQL:

```yaml
services:
  timescaledb:
    ports:
      - "5432:5432"
```

Then connect:

```bash
# Database accessible at localhost:5432
psql -h localhost -p 5432 -U postgres -d funding_tracker
```

### Run application locally with Docker database

```bash
# Start database and run migrations
docker-compose up -d timescaledb
docker-compose up db-migrate

# Run application locally (connects to Docker DB)
export DB_CONNECTION="postgresql+psycopg://postgres:postgres@localhost:5432/funding_tracker"
EXCHANGES=hyperliquid funding-tracker
```

### Override exchanges locally

Create or modify `docker-compose.override.yaml`:

```yaml
services:
  funding-tracker:
    environment:
      - EXCHANGES=hyperliquid,bybit
```

Then run normally:

```bash
docker-compose up
```

### Use local `shared` for `db-migrate`

By default, `db-migrate` uses remote context:
`https://github.com/Quantshark-tools/shared.git`.

To use local checkout (faster iteration), override build context:

```yaml
services:
  db-migrate:
    build:
      context: /path/to/quantshark/shared
      dockerfile: db-migrate/Dockerfile
```

Then rebuild:

```bash
docker-compose up --build
```

## Management

### View logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f funding-tracker
docker-compose logs -f timescaledb
docker-compose logs -f db-migrate
```

### Stop services

```bash
docker-compose down
```

### Remove volumes (deletes all data)

```bash
docker-compose down -v
```

### Rebuild after code changes

```bash
docker-compose up --build
```

## Troubleshooting

### Database connection errors

Ensure both database and migrations are healthy/successful:

```bash
docker-compose ps
```

### Application not starting

Check logs:

```bash
docker-compose logs db-migrate
docker-compose logs funding-tracker
```

### Unknown exchange IDs

Check available exchanges in main README or use `--help`:

```bash
funding-tracker --help
```
