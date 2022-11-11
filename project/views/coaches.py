"""Coach views."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from project.models import Coach


class CoachPortalView(LoginRequiredMixin, TemplateView):
    """Index view."""

    template_name = "coaches/portal.html"

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["coach"] = Coach.objects.get(profile=self.request.user.profile)
        return context
