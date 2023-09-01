#! /usr/bin/env sh
set -e

echo "Running prestart.sh"

# Let the DB start
python ./scripts/db/db_check.py

# Run migrations
alembic upgrade head

# Create initial data in DB
python ./scripts/db/initial_data.py
