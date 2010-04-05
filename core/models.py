from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from djangoratings.fields import RatingField

class Recipe(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ingredients = models.TextField()
    directions = models.TextField()
    primary_photo = models.CharField(max_length=255, blank=True)
    inserted = models.DateField(auto_now_add=True) #TODO change to DateTimeField
    tags = models.ManyToManyField('Tag', blank=True)
    servings = models.PositiveIntegerField(blank=True, null=True)
    preparation_time = models.PositiveIntegerField(blank=True, null=True)
    inserted_by = models.ForeignKey(User, null=True)
    slug = models.SlugField(unique=True, blank=True)
    rating = RatingField(range=5, allow_anonymous=False, can_change_vote=True)

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
    #TODO solve problem with this relationship - is ManyToMany but from both sides - two tables are generated :(
    #keep only attribute 'tags' on the Recipe. This attribute should return the recipes
    #like this? 
    #recipes = Recipe.objects.filter(tags__slug__exact=tag_slug)
    recipes = models.ManyToManyField('Recipe', blank=True)
    slug = models.SlugField(unique=True, blank=True)
    #TODO make some better structure later
    #order of tag in category listing. If it is negative, the Tag won't be displayed
    order = models.IntegerField(blank=True, null=False, default=9999)

    class Meta:
        ordering = ['order']

    def save(self):
        #TODO if slug already exists, assign another - increasing numbers
        self.slug = slugify(self.name)
        models.Model.save(self)

    def __unicode__(self):
        return self.name

    def recipe_count(self):
        return Recipe.objects.filter(tags__id__exact=self.id).count()


class News(models.Model):
    """
    Represents one piece of news regarding the site
    """

    #title - internal description of news. 
    title = models.CharField(max_length=100, blank=True, null=True)
    text = models.TextField()
    inserted = models.DateTimeField(auto_now_add=True)
