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
    (r'^recipes/$','core.views.recipe_list'),
    (r'^recipes/(?P<recipe_id>\d+)/$','core.views.recipe_detail'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
