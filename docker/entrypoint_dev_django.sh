#!/bin/bash
cd ebooking


python manage.py  makemigrations hotels
python manage.py  migrate hotels
python manage.py  makemigrations accounts
python manage.py  migrate accounts
python manage.py  makemigrations reservation
python manage.py  migrate reservation
python manage.py migrate
python manage.py loaddata hotels 
python manage.py loaddata hotelrooms 

python manage.py runserver 0.0.0.0:8000

exec "$@"
