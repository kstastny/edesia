from datetime import datetime
import logging

from django.contrib.sitemaps import Sitemap
from core.models import Recipe, Tag

class RecipeSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Recipe.objects.all()

    def location(self, recipe):
        return '/recipe/%s' % recipe.slug

    #http://www.sitemaps.org/protocol.php - valid priority is 0.0 to 1.0
    def priority(self, recipe):
        """
         return priority of recipe - the newer the recipe, the higher priority
        """
        recipe_age_days = datetime.now().toordinal() - recipe.inserted.toordinal() 
        #use simple linear function, will suffice
        priority = 1.0 - (recipe_age_days/14)*0.05
        if priority < 0.25:
            priority = 0.25
        logging.debug('Recipe %s is %s days old, assigned sitemap priority is %s',\
                recipe.name, recipe_age_days, priority)
        return priority

class TagSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return Tag.objects.all()

    def location(self, model):
        return '/recipes/%s' % model.slug
    
class UrlSitemap(Sitemap):

    def items(self):
        return ['/', '/about/', '/contact/', '/categories/']

    def location(self, model):
        return model

    def changefreq(self, model):
        if model in ('/'):
            return 'daily'
        else:
            return 'monthly'

#sitemaps dictionary is exported as sitemap in urls.py
sitemaps = {
        'categories': TagSitemap,
        'recipes': RecipeSitemap,
        'otherurls': UrlSitemap,
        }
