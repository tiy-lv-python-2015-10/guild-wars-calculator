from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, View, TemplateView
import requests
import json


# Create your views here.



# class MyView(View):
#     def get(self, request, *args, **kwargs):
#         return HttpResponse(response)
#         # return render(request, 'guild_wars_app/recipe_detail.html',)


class HomePageView(TemplateView):
    template_name = "guild_wars_app/recipe_list.html"

    def get_context_data(self, **kwargs):
        response = requests.get("https://api.guildwars2.com/v2/recipes/1")
        context = super(HomePageView, self).get_context_data(**kwargs)
        recipe_list = response.json()
        context['recipe_type'] = recipe_list['type']
        context['craft_time'] = recipe_list['time_to_craft_ms']
        context['disciplines'] = recipe_list['disciplines']
        return context


def recipe_detail(request, recipe_id):
    response = requests.get("https://api.guildwars2.com/v2/recipes/" + recipe_id)
    recipe_list = response.json()
    recipe_type = recipe_list['type']
    craft_time = recipe_list['time_to_craft_ms']
    disciplines = recipe_list['disciplines']

    return render(request, 'guild_wars_app/recipe_detail.html',
                  {'recipe': recipe_list, 'recipe_type': recipe_type, 'craft_time': craft_time,
                   'disciplines': disciplines})
