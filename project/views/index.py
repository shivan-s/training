"""IndexView."""

from django.views.generic import TemplateView

from project.models import Profile


class IndexView(TemplateView):
    """Index view."""

    template_name = "index.html"

    def get_context_data(self, *args, **kwargs):
        """Adding context data."""
        context = super().get_context_data(*args, **kwargs)
        # subtract 1 to exclude the admin view.
        context["count_profiles"] = Profile.objects.all().count() - 1
        return context
