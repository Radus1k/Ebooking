#!/bin/sh

cd ebooking

python manage.py  makemigrations hotels
python manage.py  migrate hotels
python manage.py  makemigrations reservation
python manage.py  migrate reservation
python manage.py loaddata hotels 
python manage.py loaddata hotelrooms 



exec "$@"