from django.shortcuts import render
import requests
from google_trans_new import google_translator
from django.contrib.auth.decorators import login_required
import os
import json
# Create your views here.

def home_function(request):
    return render(request, "index.html")

def recipe_table(request):
    return render(request,"tab.html")

def find_ingredients(request):
    """search the ingredients of a recipe"""
    API_FOOD_KEY = os.environ.get("API_FOOD_KEY")
    query = request.GET.get("json_list")
    if not query : 
        print("Rien n'est trouvé")
        print(query)
        return render(request, "list.html")
    else:  
        print("Resultat")
        # print(query)
        json_data = json.loads(query)
        # print(json_data)
        global_dict ={}
        for i in json_data:
            print(i)
            ingredient_recipe = {}
            translate_query = google_translator().translate(i,lang_tgt='en')
            # print(translate_query)
            url = "https://edamam-recipe-search.p.rapidapi.com/search"

            querystring = {"q": translate_query}
            headers = {
                'x-rapidapi-key': "API_FOOD_KEY",
                'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com"
                }
            response = requests.request("GET", url, headers=headers, params=querystring)

            recipe = response.json()["hits"]
            for label in recipe:
                recipe_dict = label["recipe"]
                name_recipe = recipe_dict["label"]
                for ingredients in recipe_dict["ingredients"]:
                    ingredient_recipe[ingredients['text']] = ingredients["weight"] 
                # print(json.dumps(ingredient_recipe, sort_keys=True, indent=4))
                print("Un de plus")
                break
            translate_response_recipe = google_translator().translate(ingredient_recipe,lang_tgt='fr')
            translate_recipe_name = google_translator().translate(recipe_dict["label"],lang_tgt='fr')
            global_dict[translate_recipe_name] = translate_response_recipe

        context = {
            "dict_recipe" : ingredient_recipe,
            "translate_response" : global_dict,
            "title_of_the_recipe" : translate_recipe_name,

        }
        print(json.dumps(global_dict, sort_keys=True, indent=4))
        return redirect(request, "list.html",context)


@login_required
def see_favorits(request):
    return render(request, "favorits.html")