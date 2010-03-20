from edesia.core.models import Recipe, Tag
from django.contrib import admin

class TagInline(admin.TabularInline):
    model = Tag
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug': ('name')}
    list_display = ('name', 'inserted', 'inserted_by', ) 
    list_filter = ('inserted', 'inserted_by', )
    list_per_page = 20

class TagAdmin(admin.ModelAdmin):
    ordering = ('name', )
    list_display = ('order', 'name', 'slug', 'recipe_count', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
