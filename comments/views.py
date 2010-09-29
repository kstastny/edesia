from django.contrib.comments.views.comments import post_comment
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib import comments
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from edesia.core.models import Recipe
from edesia.core.views import recipe_detail



def post_recipe_comment(request, next=None):
    """
        Modified method for posting comments - in case of
        errors, redirects to recipe detail
    """
    form = __get_form(request)

    #TODO make generic when necessary - when more model types than Recipe is needed
    #do this by sending POST parameter 'next_error' that will contain page
    #where user will be redirected in case of error
    if form.errors:
        #display recipe detail again, if there are some problems with comment
        data = request.POST.copy()
        object_pk = data.get("object_pk") #may be only recipe now
        recipe = Recipe.objects.get(id=object_pk)
        return recipe_detail(request, recipe.slug, form)
                

    return post_comment(request, next)


def __get_form(request):
    """
    Validates and returns the form. Modified post_comment from 
    django.contrib.comments.views.comments
    """
    # Fill out some initial data fields from an authenticated user, if present
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data["name"] = request.user.get_full_name() or request.user.username
        if not data.get('email', ''):
            data["email"] = request.user.email

    # Check to see if the POST data overrides the view's next argument.
    #next = data.get("next", next) #not necessary

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_pk = data.get("object_pk")
    if ctype is None or object_pk is None:
        return CommentPostBadRequest("Missing content_type or object_pk field.")
    try:
        model = models.get_model(*ctype.split(".", 1))
        target = model._default_manager.get(pk=object_pk)
    except TypeError:
        return CommentPostBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return CommentPostBadRequest(
            "The given content-type %r does not resolve to a valid model." % \
                escape(ctype))
    except ObjectDoesNotExist:
        return CommentPostBadRequest(
            "No object matching content-type %r and object PK %r exists." % \
                (escape(ctype), escape(object_pk)))

    # Do we want to preview the comment?
    preview = "preview" in data

    # Construct the comment form
    form = comments.get_form()(target, data=data)

    # Check security information
    if form.security_errors():
        return CommentPostBadRequest(
            "The comment form failed security verification: %s" % \
                escape(str(form.security_errors())))

    return form
