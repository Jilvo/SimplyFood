from django.test import TestCase
from django.urls import reverse,NoReverseMatch
from django.contrib.auth.models import User
from SimplyFood.wsgi import get_wsgi_application, application, os
# Create your tests here.

class PageTestCase(TestCase):
    """class PageTestCase, : Test of functions in views.py """

    def test_login_page(self):
        """test_login_page"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_signup_page(self):
        """test_signup_page"""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_404_page(self):
        """test_404_page"""
        response = self.client.get(reverse('404'))
        self.assertEqual(response.status_code, 200)

    def test_500_page(self):
        """test_500_page"""
        response = self.client.get(reverse('500'))
        self.assertEqual(response.status_code, 200)

    def test_index_page(self):
        """test_index_page"""
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

