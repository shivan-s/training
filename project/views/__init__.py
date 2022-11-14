"""Export Views."""

from .athletes import AthleteAddView, AthleteListView, YourTrainingView
from .coaches import CoachPortalView
from .index import IndexView
from .profiles import ProfileUpdateView, ProfileView

__all__ = [
    "IndexView",
    "ProfileUpdateView",
    "ProfileView",
    "CoachPortalView",
    "AthleteListView",
    "AthleteAddView",
    "YourTraininView",
]
