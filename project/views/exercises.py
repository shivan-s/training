# """Exercise business logic."""
#
# from collections import defaultdict
# from typing import Any, Literal, Union
#
# from django import forms
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import get_object_or_404, render
# from django.utils import timezone
# from django.views.generic import TemplateView
#
# from project.models import Exercise, ExerciseSet
#
#
# class ExerciseSetForm(forms.ModelForm):
#     class Meta:
#         models = ExerciseSet
#         fields = ("repetitions", "weight", "weight")
#
#
# class ExerciseView(LoginRequiredMixin, TemplateView):
#
#     template_name = "exercise/form.html"
#
#     def post(self, request, *args, **kwargs):
#         """Changing the post request.
#
#         The coach is selected to determine, which programme to display.
#         """
#         form = ProgrammeByCoachForm(request.POST)
#         if form.is_valid():
#             coach_pk = form.cleaned_data["coach"]
#             athlete = Athlete.objects.get(profile__user=request.user)
#             programmes = get_programme(athlete, level=None).filter(
#                 coach__profile__user__pk=coach_pk
#             )
#             return render(
#                 request,
#                 self.template_name,
#                 {"form": form, "programmes": programmes},
#             )
#
#         render()
