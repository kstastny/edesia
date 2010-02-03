from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

#TODO move recipe patterns to core
urlpatterns += patterns('edesia',
    # Example:
    # (r'^edesia/', include('edesia.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^recipes/$','core.views.recipe_list', {'tag_id':None}, name='recipe_list'),
    url(r'^recipes/(?P<tag_id>\d+)/$','core.views.recipe_list', name='recipe_list'),
    url(r'^recipe/(?P<recipe_id>\d+)/$','core.views.recipe_detail', name='recipe_detail'),
    url(r'^recipe/edit/$','core.views.recipe_edit', {'recipe_id':None}, name='recipe_edit'),
    url(r'^recipe/edit/(?P<recipe_id>\d+)/$','core.views.recipe_edit',name='recipe_edit'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    #TODO use different home page
    url(r'^$', 'core.views.recipe_list', {'tag_id':None}, name='home'),
)
