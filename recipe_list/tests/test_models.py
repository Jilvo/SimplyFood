from django.test import TestCase
from django.contrib.auth.models import User
from recipe_list.models import Recipe,User_Recipe_list

class RecipeModelTest(TestCase):
    def test_recipemodel(self):
        recipe = Recipe(name='Steak Teriyaki')
        self.assertEqual(str(recipe), Recipe.name)

