"""Comment admin."""

from typing import Type
from collections.abc import Iterable

from django.contrib import admin

from project.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin view."""

    model: type[Comment] = Comment
    readonly_fields: Iterable[str] = (
        "reference_id",
        "author_content_object",
        "location_content_object",
    )
    fields: Iterable[str] = (
        "reference_id",
        "content",
        "author_ct",
        "author_object_id",
        "author_content_object",
        "location_ct",
        "location_object_id",
        "location_content_object",
    )
