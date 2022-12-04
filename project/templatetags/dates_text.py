"""Custom tags to provide text output for dates if integers are given.

Additionally, give start and end dates for a week."""

from datetime import date, datetime, timedelta

from django import template
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

register = template.Library()


def _process_input(
    d: datetime | None = None,
    week: int | None = None,
    year: int | None = None,
):
    """Process input and provide errors."""
    if all([d, week, year]):
        raise ValidationError(
            _("Only datetime or week and year can be set. Not all.")
        )

    if not all([week, year]):
        raise ValidationError(_("Both week and year must be set."))


@register.simple_tag
def start_week(
    d: datetime | None = None,
    week: int | None = None,
    year: int | None = None,
) -> datetime:
    """Provide the start of the week."""

    _process_input(d=d, week=week, year=year)

    if d is not None:
        return d - timedelta(days=d.weekday())
        return week, year

    return date.fromisocalendar(year=year, week=week, day=1)


@register.simple_tag
def end_week(
    d: datetime | None = None,
    week: int | None = None,
    year: int | None = None,
) -> datetime:
    """Provide the end of the week."""

    _process_input(d=d, week=week, year=year)

    if d is not None:
        return d - timedelta(days=d.weekday() + 6)

    return date.fromisocalendar(year=year, week=week, day=7)


@register.simple_tag
def month_text(m: int) -> datetime:
    """Provide the month from an integer"""
    return datetime(year=datetime.now().year, month=m, day=1)
