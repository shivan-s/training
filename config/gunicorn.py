"""Gunicorn configuration for development and production."""

import multiprocessing
import os

from django.conf import settings

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1

if os.getenv("DJANGO_DEVELOPMENT", 0) == "1":
    # Development settings
    workers = 1
    accesslog = "-"
    access_log_format = "{'remote_ip':'%({X-Real-IP}i)s','request_id':'%({X-Request-Id}i)s','response_code':'%(s)s','request_method':'%(m)s','request_path':'%(U)s','request_querystring':'%(q)s','request_timetaken':'%(D)s','response_length':'%(B)s'}"
    reload = True
    reload_extra_files = []
    for template in settings.TEMPLATES:
        for template_dir in template["DIRS"]:  # type: ignore
            for file in template_dir.glob("**/*.html"):
                reload_extra_files.append(str(file.resolve()))

    # TODO: attemping to turn above into a list comprehension
    # reload_extra_files = [
    #     str(file.resolve())
    #     for template in TEMPLATES
    #     for template_dir in template["DIRS"]
    #     for file in template_dir.glob("**/*.html")
    # ]
