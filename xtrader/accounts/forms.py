from __future__ import unicode_literals

from collections import OrderedDict
from typing import cast

from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.utils.translation import gettext_lazy as _
from userena import settings as userena_settings
from userena.forms import SignupForm, identification_field_factory
from userena.models import UserenaSignup, UserenaManager
from userena.utils import get_profile_model

from accounts.models import Profile

attrs_dict = {"class": "required"}
USERNAME_RE = r"^[\.\w]+$"


class SignupFormExtra(SignupForm):
    """A form to demonstrate how to add extra fields to the signup form, in
    this case adding the first and last name."""

    first_name = forms.CharField(
        label=_("نام (فارسی) "), max_length=30, required=False
    )
    last_name = forms.CharField(
        label=_("نام خانوادگی (فارسی) "), max_length=30, required=False
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
        label=_("ایمیل"),
    )

    cellPhone = forms.CharField(
        label=_("تلفن همراه (اختیاری)"), max_length=30, required=False
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("رمز عبور"),
        required=True,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
        label=_("تکرار رمز "),
        required=True,
    )
    username = forms.RegexField(
        regex=USERNAME_RE,
        max_length=30,
        widget=forms.TextInput(attrs=attrs_dict),
        label=_("نام کاربری (انگلیسی)"),
    )

    def __init__(self, *args, **kw):
        """A bit of hackery to get the first name and last name at the top of
        the form instead at the end."""

        super(SignupFormExtra, self).__init__(*args, **kw)

    def save(self):
        """Override the save method to save the first and last name to the user
        field."""
        username, email, password = (
            self.cleaned_data["username"],
            self.cleaned_data["email"],
            self.cleaned_data["password1"],
        )
        userena_sign_up = cast(UserenaManager, UserenaSignup.objects)
        new_user = userena_sign_up.create_user(
            username,
            email,
            password,
            not userena_settings.USERENA_ACTIVATION_REQUIRED,
            False,
        )

        # Get the profile, the `save` method above creates a profile for each
        # user because it calls the manager method `create_user`.
        # See: https://github.com/bread-and-pepper/
        # django-userena/blob/master/userena/managers.py#L65

        new_user.first_name = self.cleaned_data["first_name"]
        new_user.last_name = self.cleaned_data["last_name"]
        # TODO: user activation by email
        new_user.save()
        p = new_user.my_profile
        p.cellPhone = self.cleaned_data["cellPhone"]
        p.save()
        # TODO: Send activation email
        signup: UserenaSignup = getattr(new_user, "userena_signup")
        signup.send_activation_email()

        # Userena expects to get the new user from this form, so return the new
        return new_user

    def clean_username(self):
        """Validate that the username is alphanumeric and is not already in
        use.

        Also validates that the username is not listed in
        ``USERENA_FORBIDDEN_USERNAMES`` list.
        """
        try:
            get_user_model().objects.get(
                username__iexact=self.cleaned_data["username"]
            )
        except get_user_model().DoesNotExist:
            pass
        else:
            if (
                userena_settings.USERENA_ACTIVATION_REQUIRED
                and UserenaSignup.objects.filter(
                    user__username__iexact=self.cleaned_data["username"]
                ).exclude(activation_key=userena_settings.USERENA_ACTIVATED)
            ):
                raise forms.ValidationError(
                    _(
                        "This username is used before but not activated,"
                        "check your email to activate."
                    )
                )
            raise forms.ValidationError(_("This username is already taken."))
        if (
            self.cleaned_data["username"].lower()
            in userena_settings.USERENA_FORBIDDEN_USERNAMES
        ):
            raise forms.ValidationError(_("This username is not allowed."))
        return self.cleaned_data["username"]

    def clean_email(self):
        """Validate that the e-mail address is unique."""
        if get_user_model().objects.filter(
            email__iexact=self.cleaned_data["email"]
        ):
            if (
                userena_settings.USERENA_ACTIVATION_REQUIRED
                and UserenaSignup.objects.filter(
                    user__email__iexact=self.cleaned_data["email"]
                ).exclude(activation_key=userena_settings.USERENA_ACTIVATED)
            ):
                raise forms.ValidationError(
                    _(
                        "This email is used before but not activated, "
                        "check your email to activate."
                    )
                )
            raise forms.ValidationError(_("This email has already used."))
        return self.cleaned_data["email"]

    def clean(self):
        MIN_LENGTH = 8
        """Validates that the values entered into the two password fields
        match.

        Note that an error here will end up in ``non_field_errors()`` because
        it doesn't apply to a single field.
        """
        if (
            "password1" in self.cleaned_data
            and "password2" in self.cleaned_data
        ):
            from django.contrib.auth.password_validation import (
                CommonPasswordValidator as cpv,
            )

            if cpv().validate(password=self.cleaned_data["password1"]):
                raise forms.ValidationError(_("This password is too common"))
            if len("password1") < MIN_LENGTH:
                raise forms.ValidationError(
                    "The new password must be at least %d characters long."
                    % MIN_LENGTH
                )
            if (
                self.cleaned_data["password1"]
                != self.cleaned_data["password2"]
            ):
                raise forms.ValidationError(_("The passwords do not match"))

        return self.cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = []


class AuthenticationForm(forms.Form):
    """A custom form where the identification can be a e-mail address or
    username."""

    identification = identification_field_factory(
        _("نام کاربری یا ایمیل"), _("نام کاربری یا ایمیل")
    )
    password = forms.CharField(
        label=_("رمز عبور"),
        widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
    )
    remember_me = forms.BooleanField(
        widget=forms.CheckboxInput(),
        required=False,
        label=_("مرا به خاطر بسپار %(days)s")
        % {"days": _(userena_settings.USERENA_REMEMBER_ME_DAYS[0])},
    )

    def __init__(self, *args, **kwargs):
        """A custom init because we need to change the label if no usernames is
        used."""
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        # Dirty hack, somehow the label doesn't get translated without
        # declaring it again here.
        self.fields["remember_me"].label = _(
            "مرا به خاطر بسپار برای %(days)s"
        ) % {"days": _("یک ماه")}
        if userena_settings.USERENA_WITHOUT_USERNAMES:
            self.fields["identification"] = identification_field_factory(
                _("ایمیل"), _("ایمیل خود را وارد کنید")
            )

    def clean(self):
        """Checks for the identification and password.

        If the combination can't be found will raise an invalid sign in
        error.
        """
        identification = self.cleaned_data.get("identification")
        password = self.cleaned_data.get("password")

        if identification and password:
            user = authenticate(
                identification=identification, password=password
            )
            from django.contrib.auth.models import User
            from django.db.models import Q

            user_qs = User.objects.filter(
                Q(username=identification) | Q(email=identification)
            )
            if not user or user_qs.count() == 0:
                raise forms.ValidationError(
                    _("username and password do not match")
                )
            if not user.is_active:
                raise forms.ValidationError(_("your account is not activated"))
        return self.cleaned_data


class EditProfileForm(forms.ModelForm):
    """Base form used for fields that are always required."""

    first_name = forms.CharField(
        label=_("نام "), max_length=30, required=False
    )
    last_name = forms.CharField(
        label=_("نام خانوادگی "), max_length=30, required=False
    )

    def __init__(self, *args, **kw):
        super(EditProfileForm, self).__init__(*args, **kw)
        # Put the first and last name at the top
        new_order = [
            ("first_name", self.fields["first_name"]),
            ("last_name", self.fields["last_name"]),
        ]
        new_order.extend(list(self.fields.items())[:-2])
        self.fields = OrderedDict(new_order)

    class Meta:
        model = get_profile_model()
        exclude = ["user", "privacy", "mugshot"]

    def save(self, commit=True):
        profile = super(EditProfileForm, self).save(commit=commit)
        # Save first and last name
        user = profile.user
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()

        return profile


class ChangeEmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)),
        label=_("New email"),
    )

    def __init__(self, user, *args, **kwargs):
        """The current ``user`` is needed for initialisation of this form so
        that we can check if the email address is still free and not always
        returning ``True`` for this query because it's the users own e-mail
        address."""
        super(ChangeEmailForm, self).__init__(*args, **kwargs)
        if not isinstance(user, get_user_model()):
            raise TypeError(
                "user must be an instance of %s" % get_user_model().__name__
            )
        else:
            self.user = user

    def clean_email(self):
        """Validate that the email is not already registered with another
        user."""
        if self.cleaned_data["email"].lower() == self.user.email:
            raise forms.ValidationError(_("شما با این ایمیل شناخته میشوید"))
        if (
            get_user_model()
            .objects.filter(email__iexact=self.cleaned_data["email"])
            .exclude(email__iexact=self.user.email)
        ):
            raise forms.ValidationError(
                _(
                    "این ایمیل در حال حاضر وجود دارد ."
                    " لطفا ایمیل جدیدی را وارد کنید"
                )
            )
        return self.cleaned_data["email"]

    def save(self):
        """Save method calls :func:`user.change_email()` method which sends out
        an email with an verification key to verify and with it enable this new
        email address."""
        signup: UserenaSignup = getattr(self.user, "userena_signup")
        return signup.change_email(
            self.cleaned_data["email"]
        )
