#coding=utf-8
import re
import logging
import random

from datetime import timedelta, datetime

from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_unicode
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from djangoratings.views import AddRatingFromModel

from models import Recipe, Tag, News
from forms import RecipeForm
from decorators import cache_func

RECIPE_PAGE_SIZE = 25

NEW_RECIPES_COUNT = 5 #count of new recipes displayed on home page
NEWS_DISPLAYED_COUNT = 3 #number of news displayed on home page
OLDEST_NEWS_DAYS = 30 #News older than this will not be displayed

#@cache_page(60*5) #TODO need *not* to cache authentication info
def index(request):

    return render_to_response('core/index.html',
            __get_index_data(),
            context_instance=RequestContext(request))


@cache_func()
def __get_index_data():
    recipes = Recipe.objects.order_by('-inserted')[:NEW_RECIPES_COUNT]
    maxdate = datetime.now() - timedelta(days=OLDEST_NEWS_DAYS)
    news = News.objects.filter(inserted__gt=maxdate).order_by('-inserted')[:NEWS_DISPLAYED_COUNT]
    if not news:
        #random_recipe = Recipe.objects.order_by('?')[0] #not using - is slow, has to do full table scan
        count = Recipe.objects.all().count()
        print count
        print random.randint(0, count - 1)
        random_recipe = Recipe.objects.all()[random.randint(0, count - 1)]
    else:
        random_recipe = None
    
    return { 'recipes': recipes, 'news' : news, 'random_recipe': random_recipe }

def searchquery(request):
    return render_to_response('core/search_result.html',
            context_instance=RequestContext(request))

@csrf_exempt
def rate_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    #send different response if it is AJAX
    response = HttpResponseRedirect(reverse('recipe_detail', \
            args=[recipe.slug]))
    if request.method == 'POST':
        rating = request.POST['rating']
        #NOTE error handling is flawed when using the view to rate, so we call the model directly
        if request.user.is_authenticated():
            recipe.rating.add(rating, request.user, request.META['REMOTE_ADDR']) 
        else:
            cookie_name = 'recipe_voted_' + str(recipe.id) 
            if cookie_name in request.COOKIES:
                pass #TODO display some message - cannot vote twice
            else:
                recipe.rating.add(rating, None, request.META['REMOTE_ADDR']) 
        if request.is_ajax():
            #send new rating to user
            response = HttpResponse('%.2f' % recipe.rating.get_real_rating())

        #do not allow the user to vote again. Not bulletproof, but sufficient
        #set the max_age for a week - parameter is in seconds
        response.set_cookie('recipe_voted_'+str(recipe.id), value=rating, max_age=604800)

    return response


def recipe_detail(request, recipe_slug, commentform=None):
    r = get_object_or_404(Recipe, slug=recipe_slug)
    #normalize line breaks - see django.utils.html.linebreaks
    ingredients = re.sub(r'\r\n|\r|\n','\n', force_unicode(r.ingredients))
    ingredient_list = re.split('\n{1,}',ingredients.strip())

    if request.user.is_authenticated():
        vote = r.rating.get_rating_for_user(request.user, None)
    else:
        #read data from cookie if specified
        cookie_name = 'recipe_voted_' + str(r.id) 
        if cookie_name in request.COOKIES:
            vote = request.COOKIES[cookie_name]
        else:
            vote = None

    can_vote = 0
    if request.user.is_authenticated():
        can_vote = 1
    else:
        #anonymous can vote only if he has not voted yet AND the anonymous voting limit is not exceeded
        can_vote = r.rating.accept_anonymous_votes(request.META['REMOTE_ADDR']) and \
                not vote

    context_dictionary = {'recipe': r,
             'ingredient_list': ingredient_list,
             'can_modify': request.user.can_modify(r),
             'vote': vote,
             'can_vote': can_vote}

    if commentform:
        #display updated comment
        #print commentform
        context_dictionary.update({
            'comment': commentform.data.get('comment',''),
            'commentform': commentform
            })
        #recipe_comments

    return render_to_response('core/recipe.html', 
            context_dictionary,
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

    #TODO if there's GET parameter tag, check that tag in 'category selection'
    if 'tag' in request.GET:
        #http://www.mail-archive.com/django-users@googlegroups.com/msg67842.html
        try:
            tag = Tag.objects.get(slug=request.GET['tag'])
            if tag:
                form.fields['tags'].initial = [tag.id]
        except Tag.DoesNotExist, e:
            logging.warn('Error loading tag [%s]: %s', request.GET['tag'], e)

    return render_to_response('core/recipe_edit.html', 
            {'form': form}, 
            context_instance=RequestContext(request))

def category_list(request):
    tags = Tag.objects.filter(order__gt=0)

    #TODO sort somehow

    #ignore categories without recipes - can be removed later when enoug recipes are present
    tags = [tag for tag in tags if tag.recipe_count() > 0]

    split_index = (len(tags)+1)/2
    return render_to_response('core/category_list.html',
            { 'tags_first' : tags[:split_index],
                'tags_second' : tags[split_index:]},
            context_instance=RequestContext(request))
