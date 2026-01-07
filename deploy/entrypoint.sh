#!/bin/bash
set -e

echo "Running database migrations..."
alembic upgrade head

echo "Starting funding tracker..."
exec funding-tracker