"""Primarily used in the navbar page to determine in the current page is the \
        active page. `is_active` is added to the css classes."""

from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def get_active_class(context, url_to_check: str) -> str:
    """Provide the `is-active` css class"""
    request = context["request"]
    if request.get_full_path() == reverse(url_to_check):
        return "is-active"
    return ""
