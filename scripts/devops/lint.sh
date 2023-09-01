#!/usr/bin/env bash

set -x

mypy app
black app --check
isort --check-only app
flake8 app

# For Core
mypy core
black core --check
isort --check-only core
flake8 core
