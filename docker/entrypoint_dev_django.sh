#!/bin/bash
cd ebooking

python manage.py loaddata hotels 
python manage.py loaddata hotelrooms 
python manage.py makemigrations hotels
python manage.py migrate hotels
python manage.py migrate

python manage.py runserver 0.0.0.0:8000

exec "$@"
