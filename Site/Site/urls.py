"""
Definition of urls for Site.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^alternatives.html', app.views.findAlternatives, name='alternatives'),
    url(r'^passed.html', app.views.showPassed, name='alternatives'),
    url(r'^mlextras.html', app.views.showMLExtras, name='mlextras'),
    url(r'^rejected.html', app.views.findMLRejections, name='rejected'),
    url(r'^recordByEID.html', app.views.viewRecordByEnterpriseId, name='viewRecordByEnterpriseId'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
