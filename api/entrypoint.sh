#!/bin/sh

echo "Waiting for postgres..."

#while ! timeout 5 bash -c "</dev/tcp/${POSTGRES_HOST}/${POSTGRES_PORT}"; do
#    sleep 0.1
#done

echo "PostgreSQL started"

python manage.py migrate
# TODO: gunicorn
python manage.py runserver 0.0.0.0:8000

exec "$@"
