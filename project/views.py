"""Views for project."""

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """Index view."""

    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        context["count_athletes"] = 1
        context["count_coaches"] = 1
        context["count_teams"] = 1
        return context
