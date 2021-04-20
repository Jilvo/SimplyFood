import sys
import os
sys.path.append(f"{os.getcwd()}/SimplyFood/")
from django.test import TestCase
import unittest
from django.urls import reverse, NoReverseMatch,resolve
from django.contrib.auth.models import User
from SimplyFood.wsgi import get_wsgi_application, application, os
from recipe_list.models import Recipe, User_Recipe_list
from recipe_list import views as recipe_list_views
from manage_user import views as manage_user_views

# Create your tests here.


class ListTest(TestCase):
    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create_user(
            "Chevy Chase", "chevyspassword", "chevy@chase.com"
        )
        self.user_2 = User.objects.create_user(
            "Jim Carrey", "jimspassword", "jim@carrey.com"
        )
        self.steak = Recipe.objects.create(
            name="Steak Teriyaki", description_list="description_bla_bla"
        )
        self.poulet = Recipe.objects.create(
            name="Poulet Persan", description_list="description_bla"
        )
        self.macaroni = Recipe.objects.create(
            name="Macaroni Cheese", description_list="c'est des pâtes"
        )
        self.list = User_Recipe_list.objects.create(
            user_name=self.user_1, list_recipe="['Steak Teriyaki ', 'Poulet persan ']"
        )

    def test_simple_recipe(self):
        """test if a recipe exist"""
        test_steak = Recipe.objects.filter(name="Steak Teriyaki")
        t_t = test_steak[0]
        self.assertEqual("Steak Teriyaki", t_t.name)
        self.assertEqual("description_bla_bla", t_t.description_list)

    def test_not_existing_recipe(self):
        """test if a recipe don't exist"""
        test_none = Recipe.objects.filter(name__contains="Tiramisu")
        t_t = test_none
        self.assertEqual("<QuerySet []>", str(t_t))

    def test_user_list(self):
        """""test the list of a user"""
        test_list = User_Recipe_list.objects.get(user_name=self.user_1)
        t_t = test_list
        self.assertEqual("['Steak Teriyaki ', 'Poulet persan ']", t_t.list_recipe)

    def test_add_list(self):
        """test_add_list"""
        test_add_list = User_Recipe_list.objects.create(
            user_name=self.user_1,
            list_recipe="['Steak Teriyaki ', 'Poulet persan ','Macaroni Cheese']",
        )
        test_add_list.save()
        test_find_list = User_Recipe_list.objects.get(
            list_recipe="['Steak Teriyaki ', 'Poulet persan ','Macaroni Cheese']"
        )
        t_t = test_find_list
        print(t_t)
        self.assertEqual("Chevy Chase", str(t_t.user_name))


class PageTestCase(TestCase):
    """class PageTestCase, : Test of functions in views.py """

    def test_404_page(self):
        """test_404_page"""
        response = self.client.get(reverse("404"))
        self.assertEqual(response.status_code, 200)

    def test_500_page(self):
        """test_500_page"""
        response = self.client.get(reverse("500"))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        """test_login_page"""
        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        """test_signup_page"""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_myaccount_page(self):
        """test_myaccount_page"""
        response = self.client.get(reverse("myaccount"))
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        """test_index_page"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_table_page(self):
        """"test_recipe_table_page"""
        response = self.client.get(reverse("tab"))
        self.assertEqual(response.status_code, 200)

    def test_legal_mention_page(self):
        """"test_legal_mention_page"""
        response = self.client.get(reverse("legal_mention"))
        self.assertEqual(response.status_code, 200)


class NoReverse(TestCase):
    """Class NoReverse"""

    def test_fake_page(self):
        """test fake page"""
        try:
            response = self.client.get(reverse("fake"))
            self.assertRaisesMessage(NoReverseMatch, response)
        except NoReverseMatch:
            pass


class RegisterTestCase(TestCase):
    """ class StatusTestCase """

    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create_user(
            "Chevy Chase", "chevyspassword", "chevy@chase.com"
        )
        self.user_2 = User.objects.create_user(
            "Jim Carrey", "jimspassword", "jim@carrey.com"
        )
        self.user = {
            "username": "Jilvotest",
            "password": "test",
            "email": "Jilvo@test.com",
        }
        self.user_wrong_email = {
            "username": "Jilvotest2",
            "password": "test",
            "email": "Jilvo",
        }
        self.user_wrong_pwd = {
            "username": "Jilvotest3",
            "password": "",
            "email": "Jilvo@gmail.com",
        }
        self.register_url = reverse("signup")
        self.login_url = reverse("login")

    def test_login(self):
        """test_login """
        response = self.client.post(
            reverse("index"),
            {"username": "chevy@chase.com", "password": "chevyspassword"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_invalid_user(self):
        """test fake user"""
        response = self.client.login(username="fake", password="fake")
        self.assertFalse(response)

    def test_register_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)

    def test_can_register_user(self):
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 200)

    def test_cant_register_user_with_unmatching_passwords(self):
        response = self.client.post(
            self.login_url, self.user_wrong_pwd, format="text/html"
        )
        self.assertEqual(response.status_code, 302)

    def test_cant_register_user_with_invalid_email(self):
        response = self.client.post(
            self.login_url, self.user_wrong_email, format="text/html"
        )
        self.assertEqual(response.status_code, 302)

    def test_cant_register_user_with_taken_email(self):
        self.client.post(self.register_url, self.user, format="text/html")
        response = self.client.post(self.register_url, self.user, format="text/html")
        self.assertEqual(response.status_code, 200)


class OsTest(TestCase):
    """Class os"""

    def test_wsgi(self):
        """test wsgi"""
        self.assertEqual(type(application), type(get_wsgi_application()))
