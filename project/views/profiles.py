"""Views for profile."""

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

from project.forms import ProfileUpdateForm

User = get_user_model()


class ProfileView(LoginRequiredMixin, TemplateView):
    """Profile view for the user.

    Only viewable if the user is authenticated.

    Users `user` context under the hood.
    """

    template_name = "profile/profile.html"
    model = User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Editing a profile view for the user.

    Only viewable if the user is authenticated.
    """

    template_name = "profile/update.html"
    form_class = ProfileUpdateForm
    success_url = reverse_lazy("project:profile")

    def get_object(self, queryset=None):
        """Overwrite the `get_object` method to obtain current authenticated \
                user."""
        return User.objects.get(pk=self.request.user.pk)
