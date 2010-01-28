from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode
from django.template import RequestContext
from models import Recipe
import re

def recipe_detail(request, recipe_id):
    r = get_object_or_404(Recipe, pk=recipe_id)
    #normalize line breaks - see django.utils.html.linebreaks
    ingredients = re.sub(r'\r\n|\r|\n','\n', force_unicode(r.ingredients))
    ingredient_list = re.split('\n{1,}',ingredients)
    
    """ 
    print ingredients
    print ingredient_list

    ingredient_list = ['a','b','c']
    """
    #TODO remove empty rows
            
    return render_to_response('core/recipe.html', 
            {'recipe': r,
             'ingredient_list': ingredient_list},
            context_instance=RequestContext(request))
