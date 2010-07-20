from django.contrib.sitemaps import Sitemap
from core.models import Recipe, Tag

class RecipeSitemap(Sitemap):
    changefreq = 'monthly'

    def items(self):
        return Recipe.objects.all()

    def location(self, recipe):
        return '/recipe/%s' % recipe.slug

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
