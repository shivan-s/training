"""Forms for registration."""

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
from django.forms.utils import ErrorList

from users.models import CustomUser

INPUT_STYLE = {"class": "input my-2"}
INPUT_ERROR_STYLE = {"class": "input my-2 is-danger"}


class CustomUserCreationForm(UserCreationForm):
    """Customising the admin form."""

    class Meta:
        """Setting for form."""

        model = CustomUser
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    """Change the admin form."""

    class Meta:
        """Setting for form."""

        model = CustomUser
        fields = ("username", "email")


class CustomErrorList(ErrorList):
    """Custom ErrorLift to provide Bulma CSS styling."""

    def get_context(self):
        """Altering context."""
        return {"errors": self, "error_class": "has-text-danger"}


class CustomLoginForm(LoginForm):
    """Customising the Login form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
        self.error_class = CustomErrorList
        self.fields["login"].widget.attrs.update({"class": "input my-2"})
        self.fields["password"].widget.attrs.update({"class": "input my-2"})

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)
        if self.errors:
            for e in self.errors:
                self.fields[e].widget.attrs.update(
                    {"class": "input my-2 is-danger"}
                )


class CustomSignupForm(SignupForm):
    """Customising the Signup form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "input my-2"})
        self.fields["password1"].widget.attrs.update({"class": "input my-2"})
        self.fields["password2"].widget.attrs.update({"class": "input my-2"})


class CustomAddEmailForm(AddEmailForm):
    """Customising the Email Add form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "input my-2"})


class CustomChangePasswordForm(ChangePasswordForm):
    """Customising the Change Password Form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(self, *args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "input my-2"})
        self.fields["password2"].widget.attrs.update({"class": "input my-2"})


class CustomResetPasswordForm(ResetPasswordForm):
    """Customising the Reset Password Form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update({"class": "input my-2"})


class CustomResetPasswordKeyFrom(ResetPasswordKeyForm):
    """Customising the Reset Password with Key Form to include Bulma CSS \
            classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "input my-2"})
        self.fields["password2"].widget.attrs.update({"class": "input my-2"})


class CustomDisconnectForm(DisconnectForm):
    """Customising the Disconnect Form to include Bulma CSS classes."""

    def __init__(self, *args, **kwargs):
        """Initialise."""
        super().__init__(*args, **kwargs)
