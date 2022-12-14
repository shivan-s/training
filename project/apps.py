"""App configuration."""
from django.apps import AppConfig


class ProjectConfig(AppConfig):
    """App configuration."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "project"

    def ready(self):
        __import__("project.signals")
