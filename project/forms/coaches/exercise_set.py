"""Exercise Set form."""

from typing import Iterable

from django import forms

from project.forms.base import BaseCustomForm
from project.models import ExerciseSet


class ExerciseSetForm(BaseCustomForm, forms.ModelForm):
    """ExerciseSet Form nested within the ExerciseForm"""

    # TODO: exercise_type needs to be made into a search?
    def __init__(self, *args, **kwargs):
        """Overwrite."""
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].get_bound_field(self, field).css_classes(
                extra_classes="is-horizontal"
            )
            self.fields[field].widget.attrs.update({"class": "input is-small"})

        self.fields["weight"].widget.attrs.update({"step": 1})
        self.fields["weight_unit"].label = "Unit"

    class Meta:
        """Meta."""

        model: type[ExerciseSet] = ExerciseSet
        fields: Iterable[str] = (
            "sets",
            "repetitions",
            "weight",
            "weight_unit",
        )
