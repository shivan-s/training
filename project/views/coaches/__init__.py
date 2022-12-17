"""Exporting portal views."""

from .add_athlete import AddAthleteView
from .confirm_athlete import ConfirmAthleteView
from .portal import CoachPortalView
from .programme_sessions import (
    CoachProgrammeSessionListView,
    CoachProgrammeSessionUpdateView,
    hx_coach_exercise_set_update_view,
    hx_coach_exercise_update_view,
    hx_coach_programme_session_delete_view,
    hx_coach_programme_session_update_view,
    hx_coach_programme_session_week_duplicate_view,
)

__all__ = [
    "CoachPortalView",
    "AddAthleteView",
    "ConfirmAthleteView",
    "CoachProgrammeSessionListView",
    "CoachProgrammeSessionUpdateView",
    "hx_coach_exercise_set_update_view",
    "hx_coach_programme_session_update_view",
    "hx_coach_exercise_update_view",
    "hx_coach_programme_session_week_duplicate_view",
    "hx_coach_programme_session_delete_view",
]
