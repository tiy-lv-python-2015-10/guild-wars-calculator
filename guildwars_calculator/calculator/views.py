from django.shortcuts import render
from django.views.generic import TemplateView
import requests
import json


def recipes(request, req_id):
    response = requests.get('https://api.guildwars2.com/v2/recipes/{}'.format(req_id))
    recipe = response.json()
    type = recipe['type']
    time_to_craft = recipe['time_to_craft_ms']
    disciplines = recipe['disciplines']
    item_id = recipe['output_item_id']
    item_link = requests.get('https://api.guildwars2.com/v2/items/{}'.format(item_id))
    item_info = item_link.json()
    item = item_info['name']
    ingredients = recipe['ingredients']
    ingredients_name = []
    ingredient_item = requests.get('https://api.guildwars2.com/v2/items/{}'.format(ingredients))
    for ingredient in ingredients:
        ingredient_item = requests.get('https://api.guildwars2.com/v2/items/{}'.format(ingredient))
        ingredient_item_info = ingredient_item.json()['']
        ingredients_name.append(ingredient_item_info)

    return render(request, 'calculator/calculator_list.html',{'recipe':recipe, 'type':type,
                                                              'time_to_craft':time_to_craft,'disciplines': disciplines,
                                                              'name':item, 'ingredients':ingredient_item})
