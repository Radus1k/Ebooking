#!/bin/sh

cd ebooking

python manage.py  makemigrations
python manage.py  migrate
python manage.py loaddata hotels 

uwsgi --ini labmalware_uwsgi.ini

exec "$@"