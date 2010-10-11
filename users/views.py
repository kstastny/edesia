#TODO use some translated UserCreationForm - can it be localized?
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from users.forms import UserCreationForm
from users.models import UserProfile

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            user.email = form.cleaned_data['email']

            #add user to group Users
            user.groups.add(Group.objects.get(name='Users'))

            user.save()

            #p = user.get_profile()
            p = UserProfile()
            p.user = user
            #cleaned_data value is available as unicode string
            p.gender = form.cleaned_data['gender'] == 'True'
            p.save()

            #login user - after saving user object, password contains just hash,
            #that's why we use the original password from the form
            user = authenticate(username=user.username, password=form.clean_password2())

            if user:
                login(request, user)

            return HttpResponseRedirect(reverse('home'))
    else:
        form = UserCreationForm()

    return render_to_response('auth/register.html',
            {'form': form}, 
            context_instance=RequestContext(request))
