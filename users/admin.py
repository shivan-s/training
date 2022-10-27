from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """
    Custom Admin form for users
    """

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    readonly_field = ("reference_id",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "username",
                    "password",
                )
            },
        ),
        (_("Personal Information"), {"fields": ("name", "email")}),
        (
            _("Persmissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_persmissions",
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
                "fields": ("username", "name", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "name",
        "username",
    )


admin.site.register(CustomUser, CustomUserAdmin)
