#coding=utf-8
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from models import Recipe
from forms import RecipeForm

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
    #TODO remove empty rows from ingredients
            
    return render_to_response('core/recipe.html', 
            {'recipe': r,
             'ingredient_list': ingredient_list,
             'can_modify': request.user.can_modify(r) },
            context_instance=RequestContext(request))

def recipe_list(request, tag_id):
    #TODO use paging
    if tag_id:
        recipes = Recipe.objects.filter(tags__id__exact=tag_id)
    else:
        recipes = Recipe.objects.all().order_by('name')

    return render_to_response('core/recipe_list.html',
            {'recipes': recipes},
            context_instance=RequestContext(request))

def recipe_edit(request, recipe_id):
    if request.method == 'POST':
        if recipe_id:
            recipe = Recipe.objects.get(pk=recipe_id)
            if not request.user.can_modify(recipe):
                raise Exception(u'User %s cannot modify recipe %s' % \
                        (request.user, recipe))
            form = RecipeForm(request.POST, instance=recipe)
        else:
            form = RecipeForm(request.POST) # todo load instance, add to the form
        #print 'saving with id %s ' % form.instance.id
        if form.is_valid():
            #save the user if he's logged in and the recipe is new
            if request.user.is_authenticated() and not form.instance.id:
                form.instance.inserted_by = request.user
            form.save() 
            return HttpResponseRedirect(reverse('recipe_detail', \
                    args=[form.instance.id]))
        else:
            pass #TODO handle validation ???
    elif recipe_id:
        recipe = Recipe.objects.get(pk=recipe_id)
        if not request.user.can_modify(recipe):
            raise Exception(u'User %s cannot modify recipe %s' % \
                    (request.user, recipe))
        form = RecipeForm(instance=recipe)
    else:
        form = RecipeForm()

    return render_to_response('core/recipe_edit.html', 
            {'form': form}, 
            context_instance=RequestContext(request))
