from django.contrib import admin
from guild_wars_calculator.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('type', 'rec_id', 'time_to_craft_ms')