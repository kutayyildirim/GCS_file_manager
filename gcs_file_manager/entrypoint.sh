#!/bin/sh
set -euo pipefail

ROLE="${1:-}"

echo " Dependencies: installing (if needed)."

pip install --no-cache-dir -r requirements.txt

echo " Postgres bekleniyor."
until nc -z db 5432; do
  echo "⏳ PostgreSQL başlatılıyor."
  sleep 1
done
echo " Postgres erişilebilir."

if [ "$1" = "web" ]; then
    python manage.py migrate --noinput
    python manage.py collectstatic --noinput
    exec gunicorn gcs_file_manager.wsgi:application --bind 0.0.0.0:8000
elif [ "$1" = "celery" ]; then
    exec celery -A gcs_file_manager worker --loglevel=info
fi

