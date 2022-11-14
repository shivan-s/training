"""Export Views."""

from .athletes import AthleteAddView, AthleteListView
from .coaches import CoachPortalView
from .index import IndexView
from .profiles import ProfileUpdateView, ProfileView
from .programme_sessions import (
    ProgrammeSessionDetailView,
    ProgrammeSessionListView,
)

__all__ = [
    "IndexView",
    "ProfileUpdateView",
    "ProfileView",
    "CoachPortalView",
    "AthleteListView",
    "AthleteAddView",
    "ProgrammeSessionListView",
    "ProgrammeSessionDetailView",
]
