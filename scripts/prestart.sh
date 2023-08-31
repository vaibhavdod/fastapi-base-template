#! /usr/bin/env sh
set -e

echo "Running prestart.sh"

# Let the DB start
python ./scripts/db_check.py

# Run migrations
alembic upgrade head

# Create initial data in DB
# python /app/app/initial_data.py
