#coding=utf-8

from django import forms
from django.forms import ModelForm
from models import Recipe

#TODO translate fields to Czech
class RecipeForm(ModelForm):
    name = forms.CharField(label='Jméno')
    ingredients = forms.CharField(label='Přísady', widget=forms.Textarea)
    directions = forms.CharField(label='Postup', widget=forms.Textarea)
    preparation_time = forms.IntegerField(label='Doba přípravy')
    servings = forms.IntegerField(label='Počet porcí')

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'directions', 'preparation_time', \
                'servings',)
