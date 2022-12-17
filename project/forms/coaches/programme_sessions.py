"""Programme Sessions Form"""


from typing import Iterable

from django import forms

from project.forms.base import BaseCustomForm
from project.models import ProgrammeSession


class ProgrammeSessionForm(BaseCustomForm, forms.ModelForm):
    """Programme Session Form for coaches."""

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)
        self.fields["coach_notes"].widget.attrs.update(
            {"class": "textarea is-small has-fixed-size", "rows": "1"}
        )
        self.fields["session_type"].widget.attrs.update({"class": "select"})
        self.fields["date"].widget.input_type = "date"
        self.fields["date"].widget.attrs.update({"class": "input is-small"})

    class Meta:
        """Meta."""

        model: type[ProgrammeSession] = ProgrammeSession
        fields: Iterable[str] = ("date", "session_type", "coach_notes")
