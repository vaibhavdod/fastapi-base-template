#! /usr/bin/env sh

# Exit in case of error
set -e

# Create a new build
docker-compose build

# Run on fresh instance
docker-compose down -v --remove-orphans
docker-compose up -d


# Run tests
docker-compose exec -T api bash ./scripts/test/exec_tests.sh "$@"
# need to put in test case execution separately for the core module


# Stop containers
docker-compose down -v --remove-orphans
