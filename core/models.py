from django.db import models
from django.contrib.auth.models import User

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    directions = models.TextField()
    primary_photo = models.CharField(max_length=255, blank=True)
    inserted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    servings = models.PositiveIntegerField(blank='True', null=True)
    preparation_time = models.PositiveIntegerField(blank='True', null=True)
    inserted_by = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    recipes = models.ManyToManyField('Recipe', blank=True)

    def __unicode__(self):
        return self.name
