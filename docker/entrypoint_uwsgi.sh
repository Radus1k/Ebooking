#!/bin/sh

cd ebooking

python manage.py loaddata hotels 
python manage.py loaddata hotelrooms 
python manage.py  makemigrations hotels 
python manage.py makemigrations reservation
python manage.py migrate reservation
python manage.py  migrate hotels


uwsgi --ini labmalware_uwsgi.ini

exec "$@"