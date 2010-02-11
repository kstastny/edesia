from edesia.core.models import Recipe, Tag
from django.contrib import admin

class TagInline(admin.TabularInline):
    model = Tag
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    #inlines = [TagInline]
    pass


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
