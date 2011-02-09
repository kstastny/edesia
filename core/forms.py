#coding=utf-8
import logging

from django import forms
from django.forms.util import ValidationError
from django.forms import ModelForm
from models import Recipe, Tag


class RecipeForm(ModelForm):
    name = forms.CharField(label='Název')
    ingredients = forms.CharField(label='Přísady', widget=forms.Textarea, help_text="Každou součást receptu zapište na samostatný řádek.")
    directions = forms.CharField(label='Postup', widget=forms.Textarea)
    preparation_time = forms.IntegerField(label='Doba přípravy', required=False, help_text="Celé číslo udávající kolik minut trvá připravit recept.")
    servings = forms.IntegerField(label='Počet porcí', required=False)
    tags = forms.ModelMultipleChoiceField(label='Kategorie', widget=forms.CheckboxSelectMultiple,\
            queryset=Tag.objects.order_by('name'), required=False)

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
        #logging.debug('In RecipeForm.clean_name')
        #raise ValidationError('no way man')
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            return instance.name
        return self.cleaned_data.get('name', None)

    
    def unique_error_message(self, unique_check):
        if len(unique_check) == 1:
            return u'Recept s názvem "%s" již existuje. Zadejte prosím jiný název receptu.' % \
                    self.data['name']
        else:
            super(RecipeForm, self).unique_error_message(unique_check)

    #TODO use in some base form class
    def as_p(self):
        "Returns this form rendered as HTML <p>s. Modified method from django.forms"
        #normal_row, error_row, row_ender, help_text_html, errors_on_separate_row
        return self._html_output(u'<p>%(label)s %(field)s%(help_text)s</p>', u'%s', '</p>',
                u'<br /><span class="microcopy">%s</span><br />', True)


    class Meta:
        model = Recipe
        fields = ('name', 'ingredients', 'directions', 'preparation_time', \
                'servings', 'tags', )
