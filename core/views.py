#coding=utf-8
import re
import logging

from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from models import Recipe, Tag
from forms import RecipeForm

RECIPE_PAGE_SIZE = 25

NEW_RECIPES_COUNT = 5 #count of new recipes displayed on home page

def index(request):
    recipes = Recipe.objects.order_by('-inserted')[:5]

    print recipes[0].inserted

    return render_to_response('core/index.html',
            { 'recipes': recipes, },
            context_instance=RequestContext(request))


def recipe_detail(request, recipe_slug):
    r = get_object_or_404(Recipe, slug=recipe_slug)
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

def recipe_list(request, tag_slug):
    tag = None
    if tag_slug:
        recipes = Recipe.objects.filter(tags__slug__exact=tag_slug)
        tag = Tag.objects.get(slug=tag_slug)
    else:
        recipes = Recipe.objects.all()

    paginator = Paginator(recipes, RECIPE_PAGE_SIZE)

    try:
        page = int(request.GET.get('page','1'))
    except ValueError:
        page = 1

    try:
        recipe_page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        recipe_page = paginator.page(paginator.num_pages)

    return render_to_response('core/recipe_list.html',
            {'recipes': recipe_page ,
                'tag': tag},
            context_instance=RequestContext(request))


def recipe_edit(request, recipe_slug):
    if request.method == 'POST':
        if recipe_slug:
            recipe = Recipe.objects.get(slug=recipe_slug)
            if not request.user.can_modify(recipe):
                raise Exception(u'User %s cannot modify recipe %s' % \
                        (request.user, recipe))
            form = RecipeForm(request.POST, instance=recipe)
        else:
            form = RecipeForm(request.POST) # todo load instance, add to the form
        if form.is_valid():
            #save the user if he's logged in and the recipe is new
            if request.user.is_authenticated() and not form.instance.id:
                logging.debug('saving new recipe: %s', form.cleaned_data['name'])
                form.instance.inserted_by = request.user
            form.save() 
            return HttpResponseRedirect(reverse('recipe_detail', \
                    args=[form.instance.slug]))
        else:
            pass #TODO handle validation ???
    elif recipe_slug:
        recipe = Recipe.objects.get(slug=recipe_slug)
        if not request.user.can_modify(recipe):
            raise Exception(u'User %s cannot modify recipe %s' % \
                    (request.user, recipe))
        form = RecipeForm(instance=recipe)
    else:
        form = RecipeForm()

    return render_to_response('core/recipe_edit.html', 
            {'form': form}, 
            context_instance=RequestContext(request))

def category_list(request):
    tags = Tag.objects.filter(order__gt=0)

    #TODO sort somehow

    #ignore categories without recipes - can be removed later when enoug recipes are present
    tags = [tag for tag in tags if tag.recipe_count() > 0]


    return render_to_response('core/category_list.html',
            { 'tags' : tags },
            context_instance=RequestContext(request))
