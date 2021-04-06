from django.shortcuts import render
from django.http import HttpResponse
import requests
from google_trans_new import google_translator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
import os
import json

from .models import User_Recipe_list,Recipe
# Create your views here.


def home_function(request):
    return render(request, "index.html")


def recipe_table(request):
    return render(request, "tab.html")

@login_required
def call_api(request,query):
    """this function call the API, in order to obtain recipes"""
    # API_FOOD_KEY = os.environ.get("API_FOOD_KEY")
    translate_query = google_translator().translate(query, lang_tgt="en")
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q": translate_query}
    headers = {
        "x-rapidapi-key": 'API_FOOD_KEY',
        "x-rapidapi-host": "edamam-recipe-search.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response

@login_required
def find_name_recipe(request):
    """this function will auto-complete an input"""
    if request.is_ajax():    
        query = request.GET.get("term")
        print(query)
        response = call_api(request,query=query)
        list_name_recipe = []
        recipe = response.json()["hits"]
        for label in recipe:
            recipe_dict = label["recipe"]
            name_recipe = recipe_dict["label"]
            translate_response_recipe = google_translator().translate(
                name_recipe, lang_tgt="fr"
            )
            list_name_recipe.append(translate_response_recipe)
        data = json.dumps(list_name_recipe)
        print(list_name_recipe)
    else :
        data = 'fail'  

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

@login_required
def find_ingredients(request):
    """search the ingredients of a recipe"""
    query = request.GET.get("json_list")
    if not query:
        print("Rien n'est trouvé")
        # print(query)
        return render(request, "list.html")
    else:
        input_after_traduction = json.loads(query)
        global_dict = {}
        list_name_translated=[]
        for name_recipe_for_trad in input_after_traduction:
            ingredient_recipe = {}
            response = call_api(request,query=name_recipe_for_trad)
            recipe = response.json()["hits"]
            for label in recipe:
                recipe_dict = label["recipe"]
                name_recipe = recipe_dict["label"]
                for ingredients in recipe_dict["ingredients"]:
                    ingredient_recipe[ingredients["text"]] = ingredients["weight"]
                break
            translate_description_recipe = google_translator().translate(
                ingredient_recipe, lang_tgt="fr"
            )
            translate_recipe_name = google_translator().translate(
                recipe_dict["label"], lang_tgt="fr"
            )
            list_name_translated.append(translate_recipe_name)
            global_dict[translate_recipe_name] = translate_description_recipe
            # print(ingredient_recipe)
            # for recipe in ingredient_recipe:
            #     print(recipe)
            find_an_recipe_or_create_it(request,translate_recipe_name,translate_description_recipe)
        add_list_recipe_to_db(request,query)
        context = {
            "dict_recipe": ingredient_recipe,
            "translated_global_response": global_dict,
            "title_of_the_recipe": list_name_translated,
        }
        print(context)
        # print(json.dumps(global_dict, sort_keys=True, indent=4))
        # for recipe2 in global_dict:
        #     print(recipe2)
        return render(request, "list.html", context)

@login_required
def find_an_recipe_or_create_it(request,translate_recipe_name,translate_description_recipe):
    existant_recipe = Recipe.objects.filter(name=translate_recipe_name)
    if not existant_recipe:
        new_recipe = Recipe.objects.create(name=translate_recipe_name,description_list=translate_description_recipe)
        new_recipe.save()
        print(new_recipe)
    else:
        print(existant_recipe)

@login_required
def add_list_recipe_to_db(request,query):
    username = request.user
    new_user_list = User_Recipe_list.objects.create(user_name=username,list_recipe=query)
    new_user_list.save()
    print(new_user_list)

@login_required
def see_history(request):
    return render(request, "history.html")
