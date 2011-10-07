from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    # Login and Logout urls
    url(r'^accounts/login/$', 'django_cas.views.login', name='login'),
    url(r'^accounts/logout/$', 'django_cas.views.logout', name='logout'),
    
    # App Urls
    url(r'^$', 'core.views.index', name='index'),
    url(r'^current$', 'core.views.current_loans', name='current_loans'),
    url(r'^loans/add$', 'core.views.add_loan', name='add_loan'),
    url(r'^loans/(\d+)$', 'core.views.view_loan', name='view_loan'),
    url(r'^person/find$', 'core.views.find_person', name='find_person'),
    url(r'^person/add$', 'core.views.add_person', name='add_person'),
    url(r'^items/description$', 'core.views.item_description', name='item_description'),
    url(r'^loans/(\d+)/return$', 'core.views.return_loan', name='return_loan'),
    url(r'^loans/(\d+)/comment$', 'core.views.comment_loan', name='comment_loan'),
) + staticfiles_urlpatterns()
