from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Recipe(models.Model):
    """Recipe class"""
  
    name = models.CharField(max_length=100, unique=True)
    description_list = models.CharField(max_length=1000, null=False)

    def __str__(self):
        return self.name


class User_Recipe_list(models.Model):
    """Recipe_list class"""
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    list_recipe = models.CharField(max_length=1000)
    recipes = models.ManyToManyField("Recipe")

