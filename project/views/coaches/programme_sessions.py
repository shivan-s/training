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
from django.views.decorators.http import require_http_methods, require_POST
from django.views.generic import TemplateView

from project.forms import ExerciseForm, ExerciseSetForm, ProgrammeSessionForm
from project.models import Athlete, Exercise, ExerciseSet, ProgrammeSession
from project.utils import get_max_exercise_order, reorder_exercise


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
@require_POST
def hx_coach_programme_session_delete_view(request, athlete_pk, pk):
    """Deleting a programme session by a coach.

    This will also restore the programme session if it has been marked for \
            deletetion.
    """
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)
    check_programme = ProgrammeSession.objects.filter(pk=pk)
    if check_programme.exists():
        programme = check_programme.first()
        if not programme.deleted:
            programme.delete()
        else:
            programme.undelete()
        form = ProgrammeSessionForm(request.POST or None, instance=programme)
        context = {"form": form, "programme": programme}
        return render(
            request,
            "coaches/programme_sessions/partials/programme_session_form.html",
            context,
        )
    else:
        Http404()


@login_required
@require_POST
def hx_coach_programme_session_update_view(request, athlete_pk=None, pk=None):
    """Coach to update/edit/create a programme session."""
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)
    formset = {}
    check_programme = ProgrammeSession.objects.filter(pk=pk)
    if check_programme.exists():
        programme = check_programme.first()
        for exercise in programme.exercise_set.all():
            exercise_form = ExerciseForm(
                request.POST or None, instance=exercise
            )
            if formset.get(exercise_form) is None:
                formset[exercise_form] = []
            for exercise_set in exercise.intended.all():
                formset[exercise_form].append(
                    (
                        ExerciseSetForm(
                            request.POST or None, instance=exercise_set
                        ),
                        exercise_set,
                    )
                )
    else:
        programme = ProgrammeSession()
        programme.athlete = athlete
        programme.coach = request.user.coach
        programme.save()
    form = ProgrammeSessionForm(request.POST or None, instance=programme)
    context = {
        "form": form,
        "formset": formset,
        "programme": programme,
    }
    if form.is_valid():
        new_programme = form.save(commit=False)
        new_programme.save()
        context["programme"] = new_programme
        return render(
            request,
            "coaches/programme_sessions/partials/programme_session_form.html",
            context,
        )
    return render(
        request,
        "coaches/programme_sessions/partials/programme_session_form.html",
        context,
    )


def _hx_programme_common(
    pk=None,
) -> type[ProgrammeSession]:
    check_programme = ProgrammeSession.objects.filter(pk=pk)
    if check_programme.exists():
        programme = check_programme.first()
    else:
        raise Http404
    return programme


@login_required
@require_POST
def hx_coach_exercise_delete_view(
    request, athlete_pk, programme_session_pk, pk
):
    """Deleting an exercise by a coach."""
    athlete = _hx_common(request=request, athlete_pk=athlete_pk)
    programme = _hx_programme_common(pk=programme_session_pk)
    check_exercise = Exercise.objects.filter(pk=pk)
    if check_exercise.exists():
        exercise = check_exercise.first()
        if not exercise.deleted:
            exercise.delete()
        else:
            exercise.undelete()
        exercise_form = ExerciseForm(request.POST or None, instance=exercise)
        programme_session_form = ProgrammeSessionForm(
            request.POST or None, instance=programme
        )
        context = {
            "exercise_form": exercise_form,
            "exercise": exercise,
            "programme": programme,
            "form": programme_session_form,
        }
        return render(
            request,
            "coaches/programme_sessions/partials/programme_session_form.html",
            context,
        )
    else:
        Http404()


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
    else:
        exercise = Exercise()
        exercise.programme_session = programme
        exercise.order = get_max_exercise_order(programme)
        exercise.save()
        exercise_set = ExerciseSet()
        exercise_set.intended = exercise
    programme_session_form = ProgrammeSessionForm(
        request.POST or None, instance=programme
    )
    form = ExerciseForm(request.POST or None, instance=exercise)
    context = {
        "form": programme_session_form,
        "exercise_form": form,
        "exercise": exercise,
    }
    if form.is_valid():
        new_exercise = form.save(commit=False)
        if exercise is None:
            new_exercise.programme_session = programme
        new_exercise.save()
        context["exercise"] = new_exercise
        return render(
            request,
            "coaches/programme_sessions/partials/programme_session_form.html",
            context,
        )
    return render(
        request,
        "coaches/programme_sessions/partials/programme_session_form.html",
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
    programme = _hx_programme_common(pk=programme_session_pk)

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
