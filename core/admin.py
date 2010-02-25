from edesia.core.models import Recipe, Tag
from django.contrib import admin

class TagInline(admin.TabularInline):
    model = Tag
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug': ('name')}

class TagAdmin(admin.ModelAdmin):
    ordering = ('name', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
