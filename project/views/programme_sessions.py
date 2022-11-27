"""Programme Session business logic."""

from collections import defaultdict
from typing import Any, Literal, Union

from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, QuerySet
from django.db.models.functions import (
    ExtractDay,
    ExtractMonth,
    ExtractWeek,
    ExtractYear,
)
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.views.generic import TemplateView

from project.models import Athlete, Comment, ProgrammeSession


def get_programme_current_week(
    athlete: type[Athlete],
):
    """Obtain the current week for the programme."""
    programmes = (
        ProgrammeSession.objects.filter(athlete=athlete)
        .annotate(week=ExtractWeek(F("date")))
        .filter(week=timezone.now().isocalendar().week)
        .order_by("-date")
    )
    return programmes


GroupByProgrammeSession = dict[int, list[ProgrammeSession]]


class BaseProgrammeView(LoginRequiredMixin, TemplateView):
    """Base Class-based view for Programme."""

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["athlete"] = Athlete.objects.get(
            profile__user=self.request.user
        )
        return context


class ProgrammeByCoachForm(forms.Form):
    """Form for dealing with post request for the ProgrammeView.

    This for is selecting the athlete's coach.
    """

    coach = forms.CharField()


class ProgrammeSessionListView(BaseProgrammeView):
    """View for training of a logged in Athlete."""

    template_name = "programme/list.html"

    def post(self, request, *args, **kwargs):
        """Changing the post request.

        The coach is selected to determine, which programme to display.
        """
        form = ProgrammeByCoachForm(request.POST)
        if form.is_valid():
            coach_pk = form.cleaned_data["coach"]
            athlete = Athlete.objects.get(profile__user=request.user)
            programmes = get_programme(athlete, level=None).filter(
                coach__profile__user__pk=coach_pk
            )
            return render(
                request,
                self.template_name,
                {"form": form, "programmes": programmes},
            )

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        athlete = context["athlete"]
        coaches = athlete.coaches.all()
        programmes = get_programme(athlete=athlete)
        context["coaches"] = coaches
        # TODO: set ability to get a default coach view
        # If the selection is changed, this needs to reflect the displayed prgoramme
        # might have to set a param on the url?
        if coaches.last():
            default_coach = coaches.last()
            context["default_coach"] = default_coach
            context["programmes"] = programmes.filter(coach=default_coach)
        return context


# from django.views.generic.edit import FormMixin, ProcessFormView
#
#
# class MultipleFormsMixin(FormMixin):
#     """
#     A mixin that provides a way to show and handle several forms in a
#     request.
#     """
#
#     form_classes = {}  # set the form classes as a mapping
#
#     def get_form_classes(self, ):
#         return self.form_classes
#
#     def get_forms(self, form_classes):
#         return dict(
#             [
#                 (key, klass(**self.get_form_kwargs()))
#                 for key, klass in form_classes.items()
#             ]
#         )
#
#     def forms_valid(self, forms):
#         return super(MultipleFormsMixin, self).form_valid(forms)
#
#     def forms_invalid(self, forms):
#         return self.render_to_response(self.get_context_data(forms=forms))
#
#
# class ProgrammeSessionDetailForm(forms.Form, MultipleFormsMixin):
#     """Form allows athlete feedback."""
#
#     def get_form_classes(self):


class CommentForm(forms.Form):
    """Comment."""

    comment = forms.CharField()


class ProgrammeSessionDetailView(BaseProgrammeView):
    """View for the detail view of the programme."""

    template_name = "programme/detail.html"

    def post(self, request, *args, **kwargs):
        """Post."""
        form = CommentForm(request.POST)
        if form.is_valid():
            athlete = Athlete.objects.get(profile__user=request.user)
            programme = get_object_or_404(
                ProgrammeSession, reference_id=self.kwargs.get("pk")
            )
            new_comment = Comment.objects.create(
                content=form.cleaned_data["comment"],
                author_content_object=athlete,
                location_content_object=programme,
            )
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "new_comment": new_comment,
                    "programme": programme,
                },
            )
        else:
            raise Exception

    def get_context_data(self, *args, **kwargs) -> dict[str, Any]:
        """Context."""
        context = super().get_context_data(*args, **kwargs)
        athlete = context["athlete"]
        context["programme"] = get_object_or_404(
            ProgrammeSession, reference_id=self.kwargs.get("pk")
        )
        context["next_programme"] = None
        context["previous_programme"] = None

        programme_sessions = ProgrammeSession.objects.filter(athlete=athlete)
        for i, ps in enumerate(programme_sessions):
            if ps.reference_id == self.kwargs.get("pk"):
                if i > 0:
                    context["next_programme"] = programme_sessions[i - 1]
                if i < len(programme_sessions) - 1:
                    context["previous_programme"] = programme_sessions[i + 1]

        return context
