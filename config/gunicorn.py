"""Gunicorn configuration for development and production."""

import multiprocessing
import os

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    reload = True
    accesslog = "-"
