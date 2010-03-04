from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Recipe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ingredients = models.TextField()
    directions = models.TextField()
    primary_photo = models.CharField(max_length=255, blank=True)
    inserted = models.DateField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True)
    servings = models.PositiveIntegerField(blank=True, null=True)
    preparation_time = models.PositiveIntegerField(blank=True, null=True)
    inserted_by = models.ForeignKey(User, null=True)
    slug = models.SlugField(unique=True, blank=True) 

    class Meta:
        ordering = ['name']

    def save(self):
        #TODO if slug already exists, assign another - increasing numbers
        self.slug = slugify(self.name)
        models.Model.save(self)

    def __unicode__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    recipes = models.ManyToManyField('Recipe', blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self):
        #TODO if slug already exists, assign another - increasing numbers
        self.slug = slugify(self.name)
        models.Model.save(self)

    def __unicode__(self):
        return self.name
