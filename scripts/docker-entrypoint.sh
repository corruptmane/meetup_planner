#!/bin/sh

set -e

[ -n "${RUN_MIGRATIONS}" ] && alembic upgrade head

exec python -O -m app
