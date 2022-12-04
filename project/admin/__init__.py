"""Exporting admin classes."""


from .comments import CommentAdmin
from .exercise import ExerciseTypeAdmin
from .programme_sessions import ProgrammeSessionAdmin
from .teams import TeamAdmin

__all__ = [
    "TeamAdmin",
    "ProgrammeSessionAdmin",
    "CommentAdmin",
    "ExerciseTypeAdmin",
    "ExerciseCategoryAdmin",
]
