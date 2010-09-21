from django.conf.urls.defaults import *
from django.conf import settings
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'/'}, name='logout'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}, name='login'),
    url(r'^register/$', 'edesia.users.views.register', name='register'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    )

if settings.SERVE_STATIC_FILES:
    urlpatterns += patterns('',
            (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
            )

#TODO move recipe patterns to core, authentication patterns to auth
urlpatterns += patterns('edesia',
    # Example:
    # (r'^edesia/', include('edesia.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    #(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^recipes/$','core.views.recipe_list', {'tag_slug':None}, name='recipe_list'),
    url(r'^recipes/(?P<tag_slug>[\w-]+)/$','core.views.recipe_list', name='recipe_list'),
    url(r'^recipe/(?P<recipe_slug>[\w-]+)/$','core.views.recipe_detail', name='recipe_detail'),
    url(r'^recipe_edit/$','core.views.recipe_edit', {'recipe_slug':None}, name='recipe_edit'),
    url(r'^recipe_edit/(?P<recipe_slug>[\w-]+)/$','core.views.recipe_edit',name='recipe_edit'),
    url(r'^recipe_rate/(?P<recipe_id>[0-9]+)/$','core.views.rate_recipe',name='recipe_rate'),
    url(r'^recipe_comment/$', 'comments.views.post_recipe_comment', name='recipe_comment'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    url(r'^about/$', direct_to_template, {'template':'core/about.html'}),

    url(r'^query/$','core.views.searchquery', name='search_query'),


    url(r'^categories/$', 'core.views.category_list', name='category_list'),
    url(r'^$', 'core.views.index', name='home'),

)


#add sitemap
from core.sitemap import sitemaps

urlpatterns += patterns('',
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps':sitemaps}),
    )

urlpatterns += patterns('',
        (r'^contact/', include('edesia.contact.urls')),
        )
