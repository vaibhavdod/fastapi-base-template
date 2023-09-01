#!/bin/sh -e
set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
black app
isort app


autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place core --exclude=__init__.py
black core
isort core

