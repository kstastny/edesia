import logging

from django.shortcuts import render_to_response
from django.http import HttpResponseNotFound
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.comments import Comment

from edesia.djangoratings.models import Vote
from edesia.core.models import Recipe


NEW_COMMENTS_COUNT = 5
NEW_VOTES_COUNT = 5
NEW_RECIPES_COUNT = 3

def display_overview(request):
    if not request.user.is_authenticated():
        logging.warn('Unauthenticated user tried to access statistics')
        return HttpResponseNotFound(
                render_to_string(
                    '404.html',
                    {},
                    context_instance=RequestContext(request)))
    if not request.user.is_superuser:
        logging.warn('Unauthorized access to statistics by user %s', request.user)
        return HttpResponseNotFound(
                render_to_string(
                    '404.html',
                    {},
                    context_instance=RequestContext(request)))

    
    comments = Comment.objects.order_by('-submit_date')[:NEW_COMMENTS_COUNT]
    votes = Vote.objects.order_by('-date_added')[:NEW_VOTES_COUNT]
    recipes = Recipe.objects.order_by('-inserted')[:NEW_RECIPES_COUNT]

    return render_to_response(
            'statistics/statistics_overview.html',
                {
                'comments': comments,
                'votes': votes,
                'recipes': recipes,
                'recipe_count': Recipe.objects.count(),
                'hide_google_analytics':True,#do not track this page
                },
            context_instance=RequestContext(request))

def display_bug_500(request):
    """
    For testing the 500 page.
    """
    asdf
