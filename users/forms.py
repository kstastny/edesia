#coding=utf-8
import logging

from django.contrib.auth import forms as authforms
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _



class UserCreationForm(authforms.UserCreationForm):
    # use widget=forms.RadioSelect with proper formatting
    email = forms.EmailField(label='Email', required=False)
    #TODO change to radio
    gender = forms.ChoiceField(choices=((True,'Muž'),(False,'Žena')), label='Pohlaví')
            #widget=forms.RadioSelect) - displays radio, but has to be formatted properly TODO


#TODO FORMAT THE FIELDS - THE INPUTS ARE A LITTLE TOO HIGH
class UserChangeForm(forms.ModelForm):
    username = forms.CharField(label=_("Username"))
    #TODO change to radio
    gender = forms.ChoiceField(choices=((True,'Muž'),(False,'Žena')), label='Pohlaví')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", )

    #http://stackoverflow.com/questions/324477/in-a-django-form-how-to-make-a-field-readonly-or-disabled-so-that-it-cannot-be 
    def __init__(self, *args, **kwargs):

        instance = kwargs.get('instance', None)
        if instance and instance.id:
            profile = instance.get_profile()
            if profile:
                logging.debug('profile.gender = %s', profile.gender)
                #initialize non-User fields - send as initial data
                initial = kwargs.get('initial', {})
                if 'gender' not in initial:
                    #note: on web4ce, the value of profile.gender is 0/1 but we need the string 'True' or 'False'
                    initial['gender'] = profile.gender and 'True' or 'False'
                kwargs['initial'] = initial

        super(UserChangeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            #name cannot be modified once input
            field = self.fields['username']
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
            field.widget.attrs['value'] = instance.username
            field.required = False

    #otherwise the name is reset to be empty
    #TODO this seems like a bug to me (according to docs it should set these values automatically http://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method)
    def clean_username(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.username
        return self.cleaned_data.get('username', None)
