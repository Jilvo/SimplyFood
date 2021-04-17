from django.test import TestCase
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from manage_user.forms import ConnexionForm, RegistrationForm


class Form_test(TestCase):
    def test_valid_form(self):
        form_data = {
            "username": "test2",
            "password": "test2",
            "email": "test1@gmail.com",
        }
        form = RegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form_data = {
            "username": "test14",
            "pasjsword": "test1",
            "email": "test1@gmail.com",
        }
        form = RegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
