import requests
from googletrans import Translator
from google_trans_new import google_translator  
import pprint

def request_recipe():    
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/extract"

    querystring = {"url":"http://www.melskitchencafe.com/the-best-fudgy-brownies/"}

    headers = {
        'x-rapidapi-key': "1a40c2e594msh2ded76b4149b2fep16ffb7jsn3c68dce1fa6b",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    id_recipe = response.json()["id"]

def recipe_ingredients():
    url = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/1003464/ingredientWidget.json"

    headers = {
        'x-rapidapi-key': "1a40c2e594msh2ded76b4149b2fep16ffb7jsn3c68dce1fa6b",
        'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)
    for ingredient in response.json()["ingredients"]:
        print(ingredient["name"])
        metric = ingredient["amount"]
        value = metric["metric"]
        print(value["value"])
        print(value["unit"])



# def trans():
#     translator = google_translator()  
#     translate_text = google_translator() .translate('the-best-fudgy-brownies',lang_tgt='fr')  
#     print(translate_text)


def new_api():
    url = "https://edamam-recipe-search.p.rapidapi.com/search"

    querystring = {"q":"Tiramisu "}

    headers = {
        'x-rapidapi-key': "1a40c2e594msh2ded76b4149b2fep16ffb7jsn3c68dce1fa6b",
        'x-rapidapi-host': "edamam-recipe-search.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    
    recipe = response.json()["hits"]
    for label in recipe:
        recipe_dict = label["recipe"]
        name_recipe = recipe_dict["label"]
        ingredients = recipe_dict["ingredientLines"]
        print(name_recipe)
        print(ingredients)
        break
        
        
    # print(response.text)
    # pprint.pprint(response.text)
new_api()

# recipe_dict = label["recipe"]
#         name_recipe = recipe_dict["label"]
#         ingredients = recipe_dict["ingredientLines"]
#         print(name_recipe)
#         print(ingredients)
        