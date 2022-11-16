"""Forms for registration."""

from django.forms.boundfield import BoundField
from django.forms.utils import ErrorList


class CustomErrorList(ErrorList):
    """Customise `ErrorLift` to provide Bulma CSS styling for error in form."""

    def get_context(self):
        """Overwrite `get_context`.

        Provide "has-text-danger" in "error_class" context.
        """
        return {"errors": self, "error_class": "block has-text-danger"}


class CustomBoundField(BoundField):
    """Customise BoundField for tags that surround input fields."""

    def css_classes(self, extra_classes=None):
        """Overwrite `css_classes`.

        Provide extra Bulma CSS class, "field".
        """
        if extra_classes is None:
            extra_classes = "field"
        else:
            extra_classes.append("field")
        return super().css_classes(extra_classes=extra_classes)


class BaseCustomForm:
    """Customise forms to include Bulma CSS classes.

    This acts as a base class and is combined like a Mixin with the \
            underlying authentication form class.

    - "field" class is added to tags surrounding input widgets (i.e. the <p> \
            tag for `{{ form.as_p }}`).
    - "input class is added directly to the input tag of the widget."
    - Special error classes are also provides as well, when an error in the \
            form is evoked.
    """

    def __init__(self, *args, **kwargs):
        """Overwrite `__init__`."""
        super().__init__(*args, **kwargs)
        self.error_class = CustomErrorList
        for field in self.fields:
            self.fields[field].get_bound_field(self, field).css_classes(
                extra_classes="field"
            )
            self.fields[field].widget.attrs.update({"class": "input"})
        if self.errors:
            for e in self.errors:
                if e != "__all__":
                    self.fields[e].widget.attrs.update(
                        {
                            "class": f"{self.fields[e].widget.attrs['class']} is-danger"
                        }
                    )
                    self.fields[e].help_text = self.errors[e]

    def __getitem__(self, name):
        """Alter classes in tags surrounding input fields."""
        try:
            field = self.fields[name]
        except KeyError:
            raise KeyError(f"Key {name} not found in Form")
        return CustomBoundField(self, field, name)
