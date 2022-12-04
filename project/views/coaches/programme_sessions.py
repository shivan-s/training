"""Views for a coach to list their athlete's programme."""

from collections.abc import Iterable
from typing import Any

from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from project.forms.base import BaseCustomForm
from project.models import Athlete, Exercise, ExerciseSet, ProgrammeSession


class CoachProgrammeSessionListView(LoginRequiredMixin, TemplateView):
    """Programme List view of an athlete for a coach to view."""

    template_name = "coaches/programme_sessions/list.html"

    def get_context_data(self, *args, **kwargs):
        """Context."""
        context = super().get_context_data(*args, **kwargs)
        athlete_pk = self.kwargs.get("pk")
        coach = self.request.user.coach
        check_athlete = coach.athletes.filter(user__pk=athlete_pk)
        if check_athlete.exists():
            athlete = check_athlete.first()
            programmes = athlete.programmesession_set.all().group_by()
        else:
            raise PermissionDenied("Athlete not registered with Coach.")
        context["coach"] = coach
        context["programmes"] = programmes
        context["athlete"] = athlete
        return context


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
            {"class": "textarea", "rows": "1"}
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
            {"class": "textarea", "rows": "1"}
        )
        self.fields["date"].widget.input_type = "date"
        self.fields["date"].widget.attrs.update({"class": "input"})

    class Meta:
        """Meta."""

        model: type[ProgrammeSession] = ProgrammeSession
        fields: Iterable[str] = ("date", "session_type", "coach_notes")


def _hx_common(request, athlete_pk) -> type[Athlete]:
    """Common methods that are shared between function based views."""

    if not request.htmx:
        raise Http404

    check_athlete = Athlete.objects.filter(user__pk=athlete_pk)
    if check_athlete.exists():
        athlete = check_athlete.first()
    else:
        raise Http404

    # check athlete is registered under coach
    coach = request.user.coach
    check_athlete = coach.athletes.filter(user__pk=athlete_pk)
    if check_athlete.exists():
        athlete = check_athlete.first()
    else:
        raise PermissionDenied("Athlete not registered.")

    return athlete


@login_required
def hx_coach_programme_session_update_view(request, athlete_pk=None, pk=None):

    athlete = _hx_common(request=request, athlete_pk=athlete_pk)

    # check programme session
    import logging

    check_programme = ProgrammeSession.objects.filter(pk=pk)
    logging.warning(check_programme)
    if check_programme.exists():
        programme = check_programme.first()
    else:
        programme = None
    form = ProgrammeSessionForm(request.POST or None, instance=programme)
    context = {"form": form, "programme": programme}
    if form.is_valid():
        new_programme = form.save(commit=False)
        if programme is None:
            new_programme.athlete = athlete
            new_programme.coach = coach
        new_programme.save()
        context["programme"] = new_programme
        return render(
            request,
            "coaches/programme_sessions/partials/programme_session_inline.html",
            context,
        )
    return render(
        request,
        "coaches/programme_sessions/partials/programme_session_form.html",
        context,
    )


@login_required
def hx_coach_exercise_update_view(
    request, athlete_pk=None, programme_session_pk=None, pk=None
):
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)

    # check programme session exists
    check_programme = ProgrammeSession.objects.filter(pk=programme_session_pk)
    if check_programme.exists():
        programme = check_programme.first()
    else:
        raise Http404

    check_exercise = Exercise.objects.filter(pk=pk)
    if check_exercise.exists():
        exercise = check_exercise.first()
    form = ExerciseForm(request.POST or None, instance=exercise)
    context = {"form": form, "exercise": exercise}
    if form.is_valid():
        new_exercise = form.save(commit=False)
        if exercise is None:
            new_exercise.intended = programme
        new_exercise.save()
        context["exercise"] = new_exercise
        return render(
            request,
            "coaches/programme_sessions/partials/exercise_inline.html",
            context,
        )
    return render(
        request,
        "coaches/programme_sessions/partials/exercise_form.html",
        context,
    )


@login_required
def hx_coach_exercise_set_update_view():
    pass


@login_required
def hx_coach_programme_session_week_duplicate_view(request, pk=None):
    """View to duplicate a programme session by week."""

    athlete = _hx_common(request, athlete_pk=pk)

    # check the most current week to duplicate
    check_programme = ProgrammeSession.objects.filter(athlete_pk=pk).
    if check_programme.exists():
        programme = check_programme.first()
    else:
        raise Http404

    check_exercise = Exercise.objects.filter(pk=pk)
    if check_exercise.exists():
        exercise = check_exercise.first()
    form = ExerciseForm(request.POST or None, instance=exercise)
    context = {"form": form, "exercise": exercise}
    if form.is_valid():
        new_exercise = form.save(commit=False)
        if exercise is None:
            new_exercise.intended = programme
        new_exercise.save()
        context["exercise"] = new_exercise
        return render(
            request,
            "coaches/programme_sessions/partials/exercise_inline.html",
            context,
        )
    return render(
        request,
        "coaches/programme_sessions/partials/exercise_form.html",
        context,
    )
