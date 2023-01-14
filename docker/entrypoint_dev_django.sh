#!/bin/sh
cd ebooking

python manage.py loaddata hotels 
python manage.py makemigrations hotels
python manage.py migrate hotels

python manage.py runserver 0.0.0.0:8000

exec "$@"
