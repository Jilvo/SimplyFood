from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from google_trans_new import google_translator

import requests
import os
import json

from .models import Recipe, User_Recipe_list

# Create your views here.


def home_function(request):
    """Display the home page"""
    return render(request, "index.html")


def recipe_table(request):
    """Display the page, where we create the list of recipe"""
    return render(request, "tab.html")


def legal_mention(request):
    """Display Legal Mention Page"""
    return render(request, "legal_mention.html")


@login_required
def call_api(request, query):
    """this function call the API, in order to obtain recipes"""
    # API_FOOD_KEY = os.environ.get("API_FOOD_KEY")
    translate_query = google_translator().translate(query, lang_tgt="en")
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q": translate_query}
    headers = {
        "x-rapidapi-key": '1a40c2e594msh2ded76b4149b2fep16ffb7jsn3c68dce1fa6b',
        "x-rapidapi-host": "edamam-recipe-search.p.rapidapi.com",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


@login_required
def find_name_recipe(request):
    """this function will auto-complete an input"""
    if request.is_ajax():
        query = request.GET.get("term")
        response = call_api(request, query=query)
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
    else:
        data = "fail"

    mimetype = "application/json"
    return HttpResponse(data, mimetype)


@login_required
def find_ingredients(request):
    """search the ingredients of a recipe"""
    query = request.GET.get("json_list")
    if not query:
        return render(request, "list.html")
    else:
        input_after_traduction = json.loads(query)
        global_dict = {}
        list_name_translated = []
        for name_recipe_for_trad in input_after_traduction:
            ingredient_recipe = {}
            response = call_api(request, query=name_recipe_for_trad)
            recipe = response.json()["hits"]
            for label in recipe:
                recipe_dict = label["recipe"]
                for ingredients in recipe_dict["ingredients"]:
                    ingredient_recipe[ingredients["text"]] = (
                        str(round(ingredients["weight"], 2)) + " g"
                    )
                break
            translate_description_recipe = google_translator().translate(
                ingredient_recipe, lang_tgt="fr"
            )
            translate_recipe_name = google_translator().translate(
                name_recipe_for_trad, lang_tgt="fr"
            )
            list_name_translated.append(translate_recipe_name)
            global_dict[translate_recipe_name] = translate_description_recipe
            find_an_recipe_or_create_it(
                request, translate_recipe_name, translate_description_recipe
            )
        add_list_recipe_to_db(request, query)
        context = {
            "dict_recipe": ingredient_recipe,
            "translated_global_response": global_dict,
            "title_of_the_recipe": list_name_translated,
        }
        print(context)
        return redirect("list")


@login_required
def find_an_recipe_or_create_it(
    request, translate_recipe_name, translate_description_recipe
):
    """find a recipe in DB or create it if the recipe don't exist"""
    existant_recipe, created = Recipe.objects.get_or_create(
        name=translate_recipe_name,
        defaults={"description_list": translate_description_recipe},
    )


@login_required
def add_list_recipe_to_db(request, query):
    """add a list of recipe in db"""
    username = request.user
    recipe_list = query
    list_of_object = []
    recipe_remove_char = "".join(recipe_list).replace("[", "")
    recipe_remove_char = "".join(recipe_remove_char).replace("]", "")
    recipe_remove_char = "".join(recipe_remove_char).replace('"', "").split(",")
    new_user_list = User_Recipe_list.objects.create(
        user_name=username, list_recipe=recipe_remove_char
    )
    for recipe_name in recipe_remove_char:
        recipe_object = Recipe.objects.get(name=recipe_name)
        list_of_object.append(recipe_object)
        new_user_list.recipes.add(recipe_object)
    new_user_list.save()


@login_required
def see_history(request):
    """See the user's recipes history"""
    user_name = request.user
    history_list = User_Recipe_list.objects.all().filter(user_name=user_name)
    history_list = history_list[::-1][:5]
    context = {"user_name": user_name, "recipes": history_list}
    return render(request, "history.html", context)


@login_required
def see_list(request):
    """See the list of recipe"""
    user_name = request.user
    history_list2 = user_name.lists.order_by("-id").first()
    history_list = history_list2.recipes.all()
    context = {"user_name": user_name, "recipes": history_list}
    return render(request, "list.html", context)
