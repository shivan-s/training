"""Views for profile."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from project.forms import ProfileUpdateForm
from project.models import Profile


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile view for the user.

    Only viewable if the user is authenticated.

    Users `user` context under the hood.
    """

    template_name = "profile.html"
    model = Profile

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["profile"] = Profile.objects.get(user=self.request.user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Editing a profile view for the user.

    Only viewable if the user is authenticated.
    """

    template_name = "profile_update.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("project:profile")

    def get_object(self, queryset=None):
        """Overwrite the `get_object` method to obtain current authenticated \
                user."""
        return self.request.user
