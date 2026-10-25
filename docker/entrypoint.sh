#!/bin/sh
# Apply any new migrations, then run the container's command (gunicorn by default).
set -e

python manage.py migrate --noinput

exec "$@"
