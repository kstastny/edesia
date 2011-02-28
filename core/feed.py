#coding=utf-8
# 1.2.0 style not supported of web4ce
#from django.contrib.syndication.views import Feed
# pre 1.2.0 style - web4ce
# see http://docs.djangoproject.com/en/1.1/ref/contrib/syndication/
from django.contrib.syndication.feeds import Feed

from models import Recipe



FEED_RECIPES_COUNT = 10 #count of new recipes returned by the feed

class LatestRecipesFeed(Feed):

    title = "Edesia.cz - Nejnovější recepty"
    link = "/recipes/"
    description = "Poslední recepty přidané do webové kuchařky Edesia.cz"


    def items(self):
        return Recipe.objects.order_by('-inserted')[:FEED_RECIPES_COUNT]


    #ignored in pre-1.2.0
    def item_title(self, item):
        return item.name

    #ignored in pre-1.2.0
    def item_description(self, item):
        #TODO should be something better
        return item.directions

    def item_link(self, item):
        return 'http://www.edesia.cz/recipe/%s' % item.slug
