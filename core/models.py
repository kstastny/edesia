from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    directions = models.TextField()
    primary_photo = models.CharField(max_length=255, blank=True)
    inserted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    recipes = models.ManyToManyField('Recipe', blank=True)

    def __unicode__(self):
        return self.name
