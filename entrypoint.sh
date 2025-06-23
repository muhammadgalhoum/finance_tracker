#!/bin/sh

echo "⏳ Waiting for PostgreSQL at $DB_HOST:$DB_PORT..."
until nc -z "$DB_HOST" "$DB_PORT"; do
  sleep 0.5
done
echo "✅ PostgreSQL is up."

# Apply migrations
python manage.py migrate

# Start the actual service (e.g., runserver, celery, etc.)
exec "$@"
