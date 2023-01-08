#!/bin/sh
cd ebooking

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata hotels 

python manage.py runserver 0.0.0.0:8000

exec "$@"
