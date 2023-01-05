#!/bin/sh

python source/manage.py makemigrations
python source/manage.py migrate

python source/manage.py runserver 0.0.0.0:8000

exec "$@"
