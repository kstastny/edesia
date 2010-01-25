from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('edesia',
    # Example:
    # (r'^edesia/', include('edesia.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^recipes/(?P<recipe_id>\d+)/$','core.views.recipe_detail'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
