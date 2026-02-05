#!/usr/bin/env bash
set -e
# python /app/startup.py
MODE="${1:-api}"
shift || true
if [ "$MODE" = "api" ]; then
  exec uvicorn app.api.main:app --host 0.0.0.0 --port 8000
else
  exec mlscaler "$@"
fi
