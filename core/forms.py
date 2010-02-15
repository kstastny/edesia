#coding=utf-8

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
            self.fields['name'].widget.attrs['readonly'] = True
            self.fields['name'].widget.attrs['disabled'] = True

    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'directions', 'preparation_time', \
                'servings', 'tags', )
