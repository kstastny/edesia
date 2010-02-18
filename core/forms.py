#coding=utf-8
import logging

from django import forms
from django.forms import ModelForm
from models import Recipe, Tag


class RecipeForm(ModelForm):
    name = forms.CharField(label='Jméno')
    ingredients = forms.CharField(label='Přísady', widget=forms.Textarea)
    directions = forms.CharField(label='Postup', widget=forms.Textarea)
    preparation_time = forms.IntegerField(label='Doba přípravy', required=False)
    servings = forms.IntegerField(label='Počet porcí', required=False)
    tags = forms.ModelMultipleChoiceField(label='Kategorie', widget=forms.CheckboxSelectMultiple,\
            queryset=Tag.objects.all(), required=False)

    #http://stackoverflow.com/questions/324477/in-a-django-form-how-to-make-a-field-readonly-or-disabled-so-that-it-cannot-be 
    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            #name cannot be modified once input
            field = self.fields['name']
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
            field.required = False
            

    def clean_name(self):
        logging.debug('In RecipeForm.clean_name')
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.name
        return self.cleaned_data.get('name', None)

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'directions', 'preparation_time', \
                'servings', 'tags', )
