#!/usr/bin/env bash
set -e

cd ./backend/

echo "Starting flower"
exec celery -A config flower --address=0.0.0.0 --port=5555