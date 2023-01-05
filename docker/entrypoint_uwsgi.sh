#!/bin/sh

python manage.py makemigrations
python manage.py migrate

uwsgi --ini labmalware_uwsgi.ini

exec "$@"