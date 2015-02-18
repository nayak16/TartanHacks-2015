"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import patterns, url
from app.forms import BootstrapAuthenticationForm

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^index.html', 'app.views.home', name='home'),

    url(r'^new_event', 'app.views.new_event'),
    url(r'^create_event', 'app.views.create_event'),
    url(r'^event_page', 'app.views.redirectBack'),
    url(r'^edit_event', 'app.views.edit_event'),
    url(r'^log_venmo', 'app.views.log_venmo'),
    url(r'^redirect_event/', 'app.views.redirect_event'),
    url(r'^event/(?P<event_id>\w+)', 'app.views.display_event'),
    url(r'^admin/(?P<event_id>\w+)', 'app.views.admin_event'),
    url(r'^confirmation', 'app.views.confirm'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'app/login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
                'year':datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
