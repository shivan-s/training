"""Comment admin."""

from django.contrib import admin

from project.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin view."""

    model = Comment
    readonly_fields = ("reference_id",)
    fields = ("content", "content_type")
