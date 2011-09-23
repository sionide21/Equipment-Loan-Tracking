from django.conf.urls.defaults import *


urlpatterns = patterns('',
    # Login and Logout urls
    (r'^accounts/login/$', 'django_cas.views.login'),
    (r'^accounts/logout/$', 'django_cas.views.logout'),
)
