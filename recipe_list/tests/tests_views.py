from django.test import TestCase
from django.urls import reverse, NoReverseMatch
from django.contrib.auth.models import User
from SimplyFood.wsgi import get_wsgi_application, application, os
from recipe_list.models import Recipe,User_Recipe_list

# Create your tests here.


class ModelTest(TestCase):
    def setUp(self):
        # Create some users
        self.user_1 = User.objects.create_user('Chevy Chase', 'chevy@chase.com', 'chevyspassword')
        self.user_2 = User.objects.create_user('Jim Carrey', 'jim@carrey.com', 'jimspassword')
        self.user_3 = User.objects.create_user('Dennis Leary', 'dennis@leary.com', 'denisspassword')
        self.steak = Recipe.objects.create(name="Steak Teriyaki",description_list="description_bla_bla")
        self.poulet = Recipe.objects.create(name="Poulet Persan",description_list="description_bla")
        self.list = User_Recipe_list.objects.create(user_name=self.user_1,list_recipe="['Steak Teriyaki ', 'Poulet persan ']")

    def test_simple_recipe(self):
        """test if a recipe exist"""
        test_steak = Recipe.objects.filter(name="Steak Teriyaki")
        t_t = test_steak[0]
        print(t_t)
        self.assertEqual("Steak Teriyaki",t_t.name)
        self.assertEqual("description_bla_bla",t_t.description_list)

    def test_not_existing_recipe(self):
        """test if a recipe don't exist"""
        test_none = Recipe.objects.filter(name__contains="Macaroni")
        t_t = test_none
        print(t_t)
        self.assertEqual('<QuerySet []>',str(t_t))

    def test_user_list(self):
        """""test the list of a user"""
        test_list = User_Recipe_list.objects.get(user_name=self.user_1)
        t_t = test_list[0]
        print(t_t)
        self.assertEqual("['Steak Teriyaki ', 'Poulet persan ']",t_t.list_recipe)


    
        


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
                                    {'username': 'chevy@chase.com', 'password': 'chevyspassword'}, follow=True)
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