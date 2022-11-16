"""ProfileAdmin."""

from typing import Iterable, Type

import nested_admin
from django.contrib import admin
from easy_thumbnails.fields import ThumbnailerField
from easy_thumbnails.widgets import ImageClearableFileInput

from project.models import Athlete, Coach, Profile

from .base import BaseCommentInline, InlineType


class CommentInline(BaseCommentInline):
    """Comment inline."""

    ct_field = "author_ct"
    ct_fk_field = "author_object_id"
    readonly_fields: Iterable[str] = ("location_content_object", "content")


class CoachInline(nested_admin.NestedStackedInline):
    """Inline for Coach in Profile."""

    model: type[Coach] = Coach


class AthleteInline(nested_admin.NestedStackedInline):
    """Inline for Athlete in the Profile."""

    model: type[Athlete] = Athlete


@admin.register(Profile)
class ProfileAdmin(nested_admin.NestedModelAdmin):
    """Profile admin view."""

    model: type[Profile] = Profile
    search_fields: Iterable[str] = ("user__name", "user__email")
    raw_id_fields: Iterable[str] = ("user",)
    list_display: Iterable[str] = ("user",)
    fields: Iterable[str] = ("name", "avatar")
    inlines: InlineType = (
        CoachInline,
        AthleteInline,
        CommentInline,
    )
    formfield_overrides = {
        ThumbnailerField: {"widget": ImageClearableFileInput},
    }
