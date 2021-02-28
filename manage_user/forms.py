
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class ConnexionForm(AuthenticationForm):
    """ Form to log an User model, this form is passed to the login view"""

    class Meta:
        model = User
        fields = ["username", "password"]


class RegistrationForm(forms.ModelForm):
    """
    Form for registering a new account.
    """

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(user.password)  # set password properly before commit
        if commit:
            user.save()
        return user