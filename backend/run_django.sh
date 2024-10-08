#!/bin/bash

cd /app

echo @@@@@@@@@@@@@@@ preparing migrations and run pytest @@@@@@@@@@@@@@@@@@

poetry run python manage.py makemigrations
poetry run python manage.py migrate

sleep 5
poetry run python manage.py add_user
sleep 5

poetry run python manage.py cat_db

sleep 5
poetry run pytest
sleep 2

echo @@@@@@@@@@@@@@@@@@@ collecting backend static @@@@@@@@@@@@@@@@@@@@@@@

poetry run python manage.py collectstatic --noinput

echo @@@@@@@@@@@@@@@@@@@@@@@@@ run gunicorn @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

poetry run gunicorn --bind 0.0.0.0:8000 --reload backend.wsgi:application