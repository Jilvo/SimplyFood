from django.shortcuts import render
import requests
from google_trans_new import google_translator
import os
# Create your views here.

def home_function(request):
    return render(request, "index.html")

def recipe_table(request):
    return render(request,"tab.html")

def find_ingredients(request):
    """search the ingredients of a recipe"""
    API_FOOD_KEY = os.environ.get("API_FOOD_KEY")
    query = request.GET.get("query")
    print(query)
    dict_recipe = {}
    translate_query = google_translator().translate(query,lang_tgt='en')
    print(translate_query)
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q": translate_query}
    headers = {
        'x-rapidapi-key': API_FOOD_KEY,
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    recipe = response.json()["hits"]
    for label in recipe:
        recipe_dict = label["recipe"]
        name_recipe = recipe_dict["label"]
        ingredients = recipe_dict["ingredientLines"]
        dict_recipe[name_recipe] = ingredients
        print(name_recipe)
        print(ingredients)
        break

    translate_response = google_translator().translate(dict_recipe,lang_tgt='fr')
    print(translate_response)

    context = {
        "dict_recipe" : dict_recipe,
        "translate_response" : translate_response,

    }
    print(dict_recipe)
    return render(request, "list.html", context)