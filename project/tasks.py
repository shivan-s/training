from celery import shared_task

from project.models import Profile


@shared_task
def count_profiles() -> int:
    return Profile.objects.all().count()
