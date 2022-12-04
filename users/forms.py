"""Forms for registration."""

from typing import Iterable

from allauth.account.forms import (
    AddEmailForm,
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SignupForm,
)
from allauth.socialaccount.forms import DisconnectForm
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from project.forms.base import BaseCustomForm
from users.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Customising the admin form."""

    class Meta:
        """Setting for form."""

        model: type[CustomUser] = CustomUser
        fields = ("name",)


class CustomUserChangeForm(UserChangeForm):
    """Change the admin form."""

    class Meta:
        """Setting for form."""

        model: type[CustomUser] = CustomUser
        fields = ("name",)


class CustomLoginForm(BaseCustomForm, LoginForm):
    """Customise `LoginForm`."""

    ...


class CustomSignupForm(BaseCustomForm, SignupForm):
    """Customise `SignupForm`"""

    ...


class CustomAddEmailForm(BaseCustomForm, AddEmailForm):
    """Customise `AddEmail`."""

    ...


class CustomChangePasswordForm(BaseCustomForm, ChangePasswordForm):
    """Customise `ChangePasswordForm`"""

    ...


class CustomResetPasswordForm(BaseCustomForm, ResetPasswordForm):
    """Customise `ResetPasswordForm`"""

    ...


class CustomResetPasswordKeyFrom(BaseCustomForm, ResetPasswordKeyForm):
    """Customise `ResetPasswordKeyForm`"""

    ...


# TODO: update this?
class CustomDisconnectForm(DisconnectForm):
    """Customising the Disconnect Form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
