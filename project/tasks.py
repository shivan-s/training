"""Tasks for celery."""

from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.cache import cache

User = get_user_model()


@shared_task
def count_users() -> None:
    total_users = User.objects.active_users().count()
    cache.set("total_users", total_users)
