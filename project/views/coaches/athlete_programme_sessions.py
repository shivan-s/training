"""Views for a coach to list their athlete's programme."""

from typing import Any
from collections.abc import Iterable

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import TemplateView

from project.forms.base import BaseCustomForm
from project.models import Athlete, Exercise, ExerciseSet, ProgrammeSession


class BaseAthleteProgrammeSessionView(LoginRequiredMixin, TemplateView):
    def get_context_data(self, *args, **kwargs):
        """Context."""
        context = super().get_context_data(*args, **kwargs)
        athlete_pk = self.kwargs.get("pk")
        coach = self.request.user.profile.coach
        check_athlete = coach.athletes.filter(profile__user__pk=athlete_pk)
        if check_athlete.exists():
            athlete = check_athlete.first()
            programmes = athlete.programmesession_set.all()
        else:
            # TODO: write a view to state that the athlete is not listed.
            return HttpResponseForbidden()
        context["coach"] = coach
        context["programmes"] = programmes
        context["athlete"] = athlete
        return context


class AthleteProgrammeSessionListView(BaseAthleteProgrammeSessionView):
    """Programme List view for the coach."""

    template_name = "coaches/athlete_programme_list.html"


class ExerciseSetForm(BaseCustomForm, forms.ModelForm):
    """ExerciseSet Form nested within the ExerciseForm"""

    # TODO: exercise_type needs to be made into a search?

    class Meta:
        """Meta."""

        model: type[Exercise] = ExerciseSet
        fields: Iterable[str] = (
            "sets",
            "repetitions",
            "weight",
            "weight_unit",
        )


class ExerciseForm(BaseCustomForm, forms.ModelForm):
    """Exercise Form which is nested within ProgrammeSessionForm."""

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)
        self.fields["coach_notes"].widget.attrs.update(
            {"class": "textarea", "rows": "2"}
        )

    # TODO: exercise_type needs to be made into a search?

    class Meta:
        """Meta."""

        model: type[Exercise] = Exercise
        fields: Iterable[str] = ("exercise_type", "coach_notes")


class ProgrammeSessionForm(BaseCustomForm, forms.ModelForm):
    """Programme Session Form for coaches."""

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)
        self.fields["coach_notes"].widget.attrs.update(
            {"class": "textarea", "rows": "2"}
        )
        self.fields["date"].widget.input_type = "date"
        self.fields["date"].widget.attrs.update({"class": "input"})

    class Meta:
        """Meta."""

        model: type[ProgrammeSession] = ProgrammeSession
        fields: Iterable[str] = ("date", "session_type", "coach_notes")


ExerciseSetFormSet = inlineformset_factory(
    Exercise,
    ExerciseSet,
    form=ExerciseSetForm,
    fk_name="intended",
    extra=0,
    min_num=1,
)


class BaseExerciseFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.nested = ExerciseSetFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix=f"exercise_set-{form.prefix}-{ExerciseSetFormSet.get_default_prefix()}",
        )


ExerciseFormSet = inlineformset_factory(
    ProgrammeSession,
    Exercise,
    form=ExerciseForm,
    formset=BaseExerciseFormSet,
    extra=0,
    min_num=1,
)


class BaseProgrammeSessionFormSet(BaseInlineFormSet):
    """Nesting Exercise into ProgrammeSession."""

    def add_fields(self, form, index):
        super().add_fields(form, index)
        form.nested = ExerciseFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            prefix=f"exercise-{form.prefix}-{ExerciseFormSet.get_default_prefix()}",
        )


class AthleteProgrammeSessionCreateView(BaseAthleteProgrammeSessionView):
    """Coach to create a programme for an athlete."""

    template_name: str = "coaches/athlete_programme_create.html"
    ProgrammeSessionFormSet = inlineformset_factory(
        Athlete,
        ProgrammeSession,
        form=ProgrammeSessionForm,
        formset=BaseProgrammeSessionFormSet,
        extra=0,
        min_num=1,
    )

    def post(self, *args, **kwargs):
        """Post."""
        pass

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["programme_session_formset"] = self.ProgrammeSessionFormSet(
            instance=context["athlete"]
        )
        return context
