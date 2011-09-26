from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # Login and Logout urls
    url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),
    
    # App Urls
    url(r'^$', 'core.views.index'),
    url(r'^secure$', 'core.views.secure_page', name='secure_page'),
    url(r'^loans/add$', 'core.views.add_loan', name='add_loan'),
)
