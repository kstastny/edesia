from edesia.core.models import Recipe, Tag, News
from django.contrib import admin

class TagInline(admin.TabularInline):
    model = Tag
    extra = 3

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_field = {'slug': ('name')}
    list_display = ('name', 'inserted', 'inserted_by', ) 
    list_filter = ('inserted', 'inserted_by', )
    list_per_page = 50

class TagAdmin(admin.ModelAdmin):
    ordering = ('name', )
    list_display = ('order', 'name', 'slug', 'recipe_count', )

class NewsAdmin(admin.ModelAdmin):
    ordering = ('-inserted', )
    list_display = ('title', 'inserted', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(News, NewsAdmin)
