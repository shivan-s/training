"""Exporting admin classes."""


from .comments import CommentAdmin
from .exercise import ExerciseTypeAdmin
from .profiles import ProfileAdmin
from .programme_sessions import ProgrammeSessionAdmin
from .teams import TeamAdmin

__all__ = [
    "TeamAdmin",
    "ProfileAdmin",
    "ProgrammeSessionAdmin",
    "CommentAdmin",
    "ExerciseTypeAdmin",
    "ExerciseCategoryAdmin",
]
