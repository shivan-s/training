"""Exporting admin classes."""


from .athletes import AthleteAdmin
from .coaches import CoachAdmin
from .comments import CommentAdmin
from .exercise import ExerciseTypeAdmin
from .profiles import ProfileAdmin
from .programme_sessions import ProgrammeSessionAdmin
from .teams import TeamAdmin

__all__ = [
    "CoachAdmin",
    "AthleteAdmin",
    "TeamAdmin",
    "ProfileAdmin",
    "ProgrammeSessionAdmin",
    "CommentAdmin",
    "ExerciseAdmin",
    "ExerciseSetAdmin",
    "ExerciseTypeAdmin",
    "ExerciseCategoryAdmin",
]
