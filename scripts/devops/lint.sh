#!/usr/bin/env bash

set -x

mypy app
black app --check
isort --recursive --check-only app

# For Core
mypy core
black core --check
isort --recursive --check-only core
 


flake8
