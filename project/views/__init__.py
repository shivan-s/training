"""Export Views."""

from .athletes import AthleteListView
from .coaches import (
    AddAthleteView,
    AthleteProgrammeSessionCreateView,
    AthleteProgrammeSessionListView,
    CoachPortalView,
    ConfirmAthleteView,
)
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
    "ConfirmAthleteView",
    "AddAthleteView",
    "AthleteListView",
    "ProgrammeSessionListView",
    "ProgrammeSessionDetailView",
    "AthleteProgrammeSessionListView",
]
