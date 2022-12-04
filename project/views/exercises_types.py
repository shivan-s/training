"""Exercise business logic."""

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView, ListView

from project.models import ExerciseCategory, ExerciseType


class ExerciseTypeListView(LoginRequiredMixin, ListView):

    paginate_by = 20
    template_name = "exercise_types/list.html"
    model = ExerciseType

    def post(self, request, *args, **kwargs):
        """Changing the post request.

        The coach is selected to determine, which programme to display.
        """
        form = ProgrammeByCoachForm(request.POST)
        if form.is_valid():
            coach_pk = form.cleaned_data["coach"]
            athlete = Athlete.objects.get(profile__user=request.user)
            programmes = get_programme(athlete, level=None).filter(
                coach__user__pk=coach_pk
            )
            return render(
                request,
                self.template_name,
                {"form": form, "programmes": programmes},
            )


class ExerciseTypeDetailView(LoginRequiredMixin, DetailView):

    template_name = "exercise_types/detail.html"
    model = ExerciseType
