"""Export Views."""

from .athletes import AthleteListView
from .coaches import (
    AddAthleteView,
    CoachPortalView,
    CoachProgrammeSessionListView,
    CoachProgrammeSessionUpdateView,
    ConfirmAthleteView,
    hx_coach_exercise_set_update_view,
    hx_coach_exercise_update_view,
    hx_coach_programme_session_delete_view,
    hx_coach_programme_session_update_view,
    hx_coach_programme_session_week_duplicate_view,
)
from .exercises_types import ExerciseTypeDetailView, ExerciseTypeListView
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
    "ExerciseTypeListView",
    "ExerciseTypeDetailView",
    "ProgrammeSessionListView",
    "ProgrammeSessionDetailView",
    "CoachProgrammeSessionListView",
    "CoachProgrammeSessionUpdateView",
    "hx_coach_programme_session_update_view",
    "hx_coach_exercise_update_view",
    "hx_coach_exercise_set_update_view",
    "hx_coach_programme_session_week_duplicate_view",
    "hx_coach_programme_session_delete_view",
]
