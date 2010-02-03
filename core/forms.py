from django.forms import ModelForm
from models import Recipe

#TODO translate fields to Czech
class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
