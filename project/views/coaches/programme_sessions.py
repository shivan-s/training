"""Views for a coach to list their athlete's programme."""

from datetime import timedelta
from typing import Any

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import QuerySet
from django.forms.models import BaseInlineFormSet
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from project.forms import ExerciseForm, ExerciseSetForm, ProgrammeSessionForm
from project.models import Athlete, Exercise, ExerciseSet, ProgrammeSession


class CoachProgrammeSessionListView(LoginRequiredMixin, TemplateView):
    """Programme List view of an athlete for a coach to view."""

    template_name = "coaches/programme_sessions/list/list.html"

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


class CoachProgrammeSessionUpdateView(LoginRequiredMixin, TemplateView):
    """Programme Update view."""

    template_name = "coaches/programme_sessions/update/update.html"

    def get_context_data(self, *args, **kwargs):
        """Context."""
        context = super().get_context_data(*args, **kwargs)
        athlete_pk = self.kwargs.get("athlete_pk")
        coach = self.request.user.coach
        check_athlete = coach.athletes.filter(user__pk=athlete_pk)
        if check_athlete.exists():
            athlete = check_athlete.first()
            programme = get_object_or_404(
                ProgrammeSession, reference_id=self.kwargs.get("pk")
            )
            form = ProgrammeSessionForm(
                self.request.POST or None, instance=programme
            )
            formset = {}
            for exercise in programme.exercise_set.all():
                exercise_form = ExerciseForm(
                    self.request.POST or None, instance=exercise
                )
                if formset.get(exercise_form) is None:
                    formset[exercise_form] = []

                for exercise_set in exercise.intended.all():
                    formset[exercise_form].append(
                        ExerciseSetForm(
                            self.request.POST or None,
                            instance=exercise_set,
                        )
                    )
        else:
            raise PermissionDenied("Athlete not registered with Coach.")

        context["programme"] = programme
        context["coach"] = coach
        context["athlete"] = athlete
        context["form"] = form
        context["formset"] = formset
        return context


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
@require_http_methods(["DELETE"])
def hx_coach_programme_session_delete_view(request, athlete_pk, pk):
    """Deleting a programme session by a coach."""
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)
    check_programme = ProgrammeSession.objects.filter(pk=pk)
    if check_programme.exists():
        programme = check_programme.first()
        programme.delete()
        context = {"programme": programme}
        return render(
            request,
            "coaches/programme_sessions/detail/update.html",
            context,
        )
    else:
        Http404()


@login_required
def hx_coach_programme_session_update_view(request, athlete_pk=None, pk=None):
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)
    formset = {}
    check_programme = ProgrammeSession.objects.filter(pk=pk)
    if check_programme.exists():
        programme = check_programme.first()
        for exercise in programme.exercise_set.all():
            for exercise_set in exercise.intended.all():
                exercise_form = ExerciseForm(
                    request.POST or None, instance=exercise
                )
                if formset.get((exercise_form, exercise)) is None:
                    formset[(exercise_form, exercise)] = []
                formset[(exercise_form, exercise)].append(
                    (
                        ExerciseSetForm(
                            request.POST or None, instance=exercise_set
                        ),
                        exercise_set,
                    )
                )
    else:
        programme = None
    form = ProgrammeSessionForm(request.POST or None, instance=programme)
    context = {
        "form": form,
        "formset": formset,
        "programme": programme,
    }
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


def _hx_exercise_common(
    programme_session_pk=None,
) -> QuerySet[type[ProgrammeSession]]:
    check_programme = ProgrammeSession.objects.filter(pk=programme_session_pk)
    if check_programme.exists():
        programme = check_programme.first()
    else:
        raise Http404


@login_required
def hx_coach_exercise_update_view(
    request, athlete_pk=None, programme_session_pk=None, pk=None
):
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)

    # check programme_session exists
    programme = _hx_programme_common(pk=programme_session_pk)

    check_exercise = Exercise.objects.filter(pk=pk)
    if check_exercise.exists():
        exercise = check_exercise.first()
    form = ExerciseForm(request.POST or None, instance=exercise)
    context = {
        "form": form,
        "exercise": exercise,
    }
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
def hx_coach_exercise_set_update_view(
    request,
    athlete_pk=None,
    programme_session_pk=None,
    exercise_pk=None,
    pk=None,
):
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)
    programme = _hx_exercise_common(pk=programme_session_pk)

    check_exercise = Exercise.objects.filter(pk=exercise_pk)
    if check_exercise.exists():
        exercise = check_exercise.first()
    else:
        raise Http404

    check_exercise_set = ExerciseSet.objects.filter(pk=pk)
    if check_exercise_set.exists():
        exercise_set = check_exercise_set.first()
    form = ExerciseSetForm(request.POST or None, instance=exercise_set)
    context = {"form": form, "exercise_set": exercise_set}
    if form.is_valid():
        new_exercise_set = form.save(commit=False)
        if exercise_set is None:
            new_exercise_set.exercise = exercise
        new_exercise_set.save()
        context["exercise_set"] = new_exercise_set
        return render(
            request,
            "coaches/programme_session/partials/exercise_set_inline.html",
            context,
        )
    return render(
        request,
        "coaches/programme_session/partials/exercise_set_form.html",
        context,
    )


@login_required
def hx_coach_programme_session_week_duplicate_view(request, pk=None):
    """View to duplicate a programme session by week."""

    athlete = _hx_common(request, athlete_pk=pk)

    # check the most current week to duplicate
    recent_week_programmes = ProgrammeSession.objects.filter(
        athlete__pk=pk
    ).most_recent_week()
    if recent_week_programmes.exists():
        with transaction.atomic():
            for programme in recent_week_programmes:
                exercises = Exercise.objects.filter(
                    programme_session=programme.pk
                )
                programme.pk = None
                programme._state.adding = True
                programme.date += timedelta(days=7)
                programme.save()
                for exercise in exercises:
                    exercise_sets = ExerciseSet.objects.filter(
                        intended=exercise.pk
                    )
                    exercise.pk = None
                    exercise._state.adding = True
                    exercise.programme_session = programme
                    exercise.save()
                    for exercise_set in exercise_sets:
                        exercise_set.pk = None
                        exercise_set._state.adding = True
                        exercise_set.intended = exercise
                        exercise_set.save()

    else:
        raise Http404

    context = {
        "programmes": ProgrammeSession.objects.filter(
            athlete__pk=pk
        ).group_by()
    }

    return render(
        request,
        "coaches/programme_sessions/list/list.html",
        context,
    )
