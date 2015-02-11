from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.auth.hashers import is_password_usable, identify_hasher
from django.utils.html import format_html, format_html_join
from django.forms.util import flatatt
from django.template import loader
from .models import User
from project.utilities import random_generate

class ReadOnlyPasswordHashWidget(forms.Widget):
    def render(self, name, value, attrs):
        encoded = value
        final_attrs = self.build_attrs(attrs)

        if not encoded or not is_password_usable(encoded):
            summary = mark_safe("<strong>%s</strong>" % ugettext("No password set."))
        else:
            try:
                hasher = identify_hasher(encoded)
            except ValueError:
                summary = mark_safe("<strong>%s</strong>" % ugettext(
                    "Invalid password format or unknown hashing algorithm."))
            else:
                summary = format_html_join('',
                                           "<strong>{0}</strong>: {1} ",
                                           ((ugettext(key), value)
                                            for key, value in hasher.safe_summary(encoded).items())
                                           )

        return format_html("<div{0}>{1}</div>", flatatt(final_attrs), summary)


class ReadOnlyPasswordHashField(forms.Field):
    widget = ReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("required", False)
        super(ReadOnlyPasswordHashField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        # Always return initial because the widget doesn't
        # render an input field.
        return initial

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.EmailField(label=_("Username"), max_length=30,
        help_text=_("Required. 30 characters or fewer.")),
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.verify_code = random_generate()
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    username = forms.RegexField(
        label=_("Username"), max_length=30, regex=r"^[\w.@+-]+$",
        help_text=_("Required. 30 characters or fewer. Letters, digits and "
                      "@/./+/-/_ only."),
        error_messages={
            'invalid': _("This value may contain only letters, numbers and "
                         "@/./+/-/_ characters.")})
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = User
        exclude = ("id",)

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
