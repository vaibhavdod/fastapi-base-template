#!/usr/bin/env bash

set -e
set -x

# Install all dependencies
poetry install

# Set environment variables
export APP_ENV=test
export PYTHONDONTWRITEBYTECODE=1

# Run tests
poetry run pytest --cov=project_name --cov-report=term-missing tests/ "${@}"
