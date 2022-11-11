from django.core.management import call_command


def test_validate_templates():
    """Validate templates."""
    call_command("validate_templates")
