"""Signals."""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from project.models import Athlete, Coach, ExerciseSet, Profile

# allauth.account.signals.email_confirmed(request, email_address)


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    """Create profile when User instance is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def create_coach_and_athlete(sender, instance, created, **kwargs):
    """Create both Coach and Athlete instance."""
    if created:
        Coach.objects.create(profile=instance)
        Athlete.objects.create(profile=instance)
