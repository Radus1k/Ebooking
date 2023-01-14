#!/bin/sh

cd ebooking

python manage.py loaddata hotels 
python manage.py  makemigrations hotels
python manage.py  migrate hotels
# python manage.py  collectstatic --no-input --clear -v 0
echo "True"

exec "$@"