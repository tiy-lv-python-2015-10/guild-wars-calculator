from django.db import models

class Recipe(models.Model):
    type = models.CharField(max_length=50)
    output_item_id = models.IntegerField()
    output_item_count = models.IntegerField()
    min_rating = models.IntegerField()
    time_to_craft_ms = models.IntegerField()
    rec_id = models.IntegerField()
    chat_link = models.CharField(max_length=150)

    @property
    def disciplines(self):
        return self.discipline_set.all()

    @property
    def flags(self):
        return self.flag_set.all()

    @property
    def ingredients(self):
        return self.ingredient_set.all()

class Discipline(models.Model):
    name = models.CharField(max_length=40)
    recipe = models.ForeignKey(Recipe)

class Flag(models.Model):
    name = models.CharField(max_length=40)
    recipe = models.ForeignKey(Recipe)

class Ingredient(models.Model):
    item_id = models.IntegerField()
    count = models.IntegerField()
    recipe = models.ForeignKey(Recipe)
