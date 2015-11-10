from django.shortcuts import render
import requests
from guild_wars_calculator.models import Recipe, Discipline, Flag, Ingredient


def get_recipe(request, rec_id):
    """
    Check database for Recipe object. If not there, get recipe from
    API and create Recipe object, with Discipline, Flag, and Ingredient
    objects to store data. Calculate price and render display for recipe
    information.
    :param request:
    :param rec_id: id of recipe for guild wars API
    :return: render to template with recipe context
    """
    try:
        recipe = Recipe.objects.get(rec_id=rec_id)

    except:
        response = requests.get('https://api.guildwars2.com/v2/recipes/' +
                                rec_id)
        rec_dict = response.json()
        # Create Recipe and related objects based on api response
        Recipe.objects.create(
            type=rec_dict['type'],
            output_item_id=rec_dict['output_item_id'],
            output_item_count=rec_dict['output_item_count'],
            min_rating=rec_dict['min_rating'],
            time_to_craft_ms=rec_dict['time_to_craft_ms'],
            rec_id=rec_dict['id'],
            chat_link=rec_dict['chat_link']
        )
        for discipline in rec_dict['disciplines']:
            Discipline.objects.create(
                name=discipline,
                recipe=Recipe.objects.get(rec_id=rec_dict['id'])
            )
        for flag in rec_dict['flags']:
            Flag.objects.create(
                name=flag,
                recipe=Recipe.objects.get(rec_id=rec_dict['id'])
            )
        for ingredient in rec_dict['ingredients']:
            Ingredient.objects.create(
                item_id=ingredient['item_id'],
                count=ingredient['count'],
                recipe=Recipe.objects.get(rec_id=rec_dict['id'])
            )
        recipe = Recipe.objects.get(rec_id=rec_dict['id'])

    # Add data to context_dict to be passed to template
    context_dict = {}
    context_dict['type'] = recipe.type
    context_dict['time_to_craft'] = recipe.time_to_craft_ms
    context_dict['disciplines'] = recipe.discipline_set.all()
    context_dict['flags'] = recipe.flag_set.all()
    item_list = recipe.ingredient_set.all()

    # Get item and price info from guild wars api
    all_items = []
    for item in item_list:
        item_info = {}
        response2 = requests.get('https://api.guildwars2.com/v2/items/' +
                                 str(item.item_id))
        item_dict = response2.json()
        item_info['name'] = item_dict['name']
        item_info['icon'] = item_dict["icon"]

        response3 = requests.get('https://api.guildwars2.com/v2/'
                                 'commerce/prices/' + str(item.item_id))
        price_dict = response3.json()
        item_info['price'] = price_dict['buys']['unit_price']
        item_info['total'] = price_dict['buys']['unit_price'] * item.count
        item_info['sell_price'] = price_dict['sells']['unit_price']
        item_info['price_diff'] = item_info['price'] - item_info['sell_price']
        item_info['count'] = item.count
        all_items.append(item_info)

    # Calculate total price for recipe
    total_price = 0
    for item in all_items:
        total_price += item['total']

    context_dict['items'] = all_items
    context_dict['total_price'] = total_price

    return render(request, 'guild_wars_calculator/recipe_detail.html',
                  {'recipe': context_dict})
