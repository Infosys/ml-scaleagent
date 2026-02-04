#!/bin/sh
set -e

# Run tests before starting the app
pytest tests

exec "$@"
