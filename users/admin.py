"""Admin for user model."""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    """Custom Admin form for users."""

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()
    readonly_fields = ("reference_id",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "reference_id",
                    "username",
                    "password",
                )
            },
        ),
        (_("Personal Information"), {"fields": ("email",)}),
        (
            _("Persmissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "reference_id",
        "email",
    )
