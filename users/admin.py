"""Admin for user model."""

from typing import Iterable

import nested_admin
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.widgets import ImageClearableFileInput

"""TeamAdmin."""

from project.admin.base import BaseCommentInline, InlineType
from project.models import Athlete, Coach

from .forms import CustomUserChangeForm, CustomUserCreationForm

User = get_user_model()


class CommentInline(BaseCommentInline):
    """Comment Inline."""

    ct_field = "author_ct"
    ct_fk_field = "author_object_id"
    readonly_fields: Iterable[str] = ("location_content_object", "content")


class CoachInline(nested_admin.NestedStackedInline):
    """Inline for Coach in Profile."""

    model: type[Coach] = Coach


class AthleteInline(nested_admin.NestedStackedInline):
    """Inline for Athlete in the Profile."""

    model: type[Athlete] = Athlete


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    """Custom Admin form for users."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    search_fields: Iterable[str] = ("name", "email")
    readonly_fields: Iterable[str] = ("reference_id",)
    fieldsets: Iterable = (
        (
            None,
            {
                "fields": (
                    "reference_id",
                    "password",
                )
            },
        ),
        (_("Personal Information"), {"fields": ("name", "avatar", "email")}),
        (
            _("Persmissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("password1", "password2"),
            },
        ),
    )

    inlines: InlineType = (
        CoachInline,
        AthleteInline,
        CommentInline,
    )

    formfield_overrides = {
        ThumbnailerField: {"widget": ImageClearableFileInput},
    }
