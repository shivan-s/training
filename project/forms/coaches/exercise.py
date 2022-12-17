"""Exercise form."""

from typing import Iterable

from django import forms

from project.forms.base import BaseCustomForm
from project.models import Exercise


class ExerciseForm(BaseCustomForm, forms.ModelForm):
    """Exercise Form which is nested within ProgrammeSessionForm."""

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)
        self.fields["coach_notes"].widget.attrs.update(
            {"class": "textarea is-small has-fixed-size", "rows": "1"}
        )

    # TODO: exercise_type needs to be made into a search?

    class Meta:
        """Meta."""

        model: type[Exercise] = Exercise
        fields: Iterable[str] = ("exercise_type", "coach_notes")
