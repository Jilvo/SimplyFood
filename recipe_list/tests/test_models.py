from django.test import TestCase
from django.contrib.auth.models import User
from catalog.models import Recipe,User_Recipe_list

class RecipeModelTest(TestCase):
    def test_recipemodel(self):
        recipe = Recipe(name='Steak Teriyaki')
        self.assertEqual(str(recipe), Recipe.name)