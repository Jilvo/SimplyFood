from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from SimplyFood.wsgi import get_wsgi_application, application, os

# Create your tests here.


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
        response = self.client.get(reverse("login"))
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
            response = self.client.get(reverse('fake'))
            self.assertRaisesMessage(NoReverseMatch, response)
        except NoReverseMatch:
            pass


class StatusTestCase(TestCase):
    """ class StatusTestCase """
    def test_login(self):
        """test_login """
        response = self.client.post(reverse('index'),
                                    {'username': 'testuser', 'password': 'password'}, follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_user(self):
        """test fake user"""
        response = self.client.login(username="fake", password="fake")
        self.assertFalse(response)

class OsTest(TestCase):
    """Class os"""
    def test_wsgi(self):
        """test wsgi"""
        self.assertEqual(type(application), type(get_wsgi_application()))