"""Exporting exercise admins."""

from .exercise_categories import ExerciseCategoryAdmin
from .exercise_sets import ExerciseSetAdmin
from .exercise_types import ExerciseTypeAdmin
from .exercises import ExerciseAdmin

__all__ = [
    "ExerciseCategoryAdmin",
    "ExerciseTypeAdmin",
    "ExerciseAdmin",
    "ExerciseSetAdmin",
]
