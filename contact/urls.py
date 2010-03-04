from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^thankyou/$', 'contact.views.thankyou', name='contact_thankyou'),
    (r'^$', 'contact.views.contactview'),
    )
