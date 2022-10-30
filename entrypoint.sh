#!/bin/bash
python manage.py makemigrations --no-input
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py tailwind build

gunicorn config.wsgi
