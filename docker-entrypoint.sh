#!/bin/sh
cd /code 

python manage.py migrate
python manage.py collectstatic --no-input
gunicorn -c python:config.gunicorn config.wsgi
