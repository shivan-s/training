"""Manager for CustomUser model."""

from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Q


class CustomerUserQuerySet(models.QuerySet):
    """CustomUser QuerySet."""

    def active_users(self) -> models.QuerySet:
        """Active users.

        Excludes anonymous user and admin account.
        """
        return self.filter(Q(is_superuser=False), ~Q(email="AnonymousUser"))


class CustomUserManager(UserManager):
    """CustomerUser Manager."""

    def get_queryset(self) -> type[CustomerUserQuerySet]:
        """Redefine queryset."""
        return CustomerUserQuerySet(self.model, using=self._db)

    def active_users(self) -> models.QuerySet:
        """Determine the number of users"""
        return self.get_queryset().active_users()

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("Please provide an e-mail.")

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email=None, password=None, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email=None, password=None, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self._create_user(email, password, **kwargs)
