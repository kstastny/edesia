#coding=utf-8
from django.contrib.auth import forms as authforms
from django import forms

class UserCreationForm(authforms.UserCreationForm):
    # use widget=forms.RadioSelect with proper formatting
    gender = forms.ChoiceField(choices=((True,'Muž'),(False,'Žena')), label='Pohlaví')