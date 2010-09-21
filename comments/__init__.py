from forms import CommentForm
from django.core.urlresolvers import reverse


def get_form():
    return CommentForm


def get_form_target():
    #TODO works only if comments are used just for recipes
    return reverse('recipe_comment')
