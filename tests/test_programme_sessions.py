"""Programme Session tests."""


def test_set_successful(exercise_set):
    """Test if a set was successful."""
    assert exercise_set.intended != exercise_set.outcome
    exercise_set.set_successful()
    assert exercise_set.intended == exercise_set.outcome
