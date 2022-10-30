#!/bin/bash
python manage.py makemigrations --no-input
python manage.py migrate
python manage.py collectstatic --no-input

gunicorn config.wsgi:application --workers 1 --bind 0.0.0.0:8000 --log-level debug
