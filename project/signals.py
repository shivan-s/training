"""Signals."""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import Athlete, Coach, ExerciseSet

# allauth.account.signals.email_confirmed(request, email_address)


@receiver(post_save, sender=get_user_model())
def create_coach_and_athlete(sender, instance, created, **kwargs):
    """Create both Coach and Athlete instance from the user creation."""
    if created:
        Coach.objects.create(user=instance)
        Athlete.objects.create(user=instance)
        instance.coach.athletes.add(instance.athlete)
        instance.athlete.coaches.add(instance.coach)
