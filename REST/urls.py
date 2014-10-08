#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()


# All view functions here must be in '/views/views.py'
urlpatterns = patterns('REST',
    # url(r'^docs/', include('docs.urls')),
    (r'^$', 'jchem_rest.doc'),  # Landing page
    (r'^getChemDeats/?$', 'jchem_rest.getChemDeats'),
    (r'^mrvToSmiles/?$', 'jchem_rest.mrvToSmiles'),
    (r'^getChemSpecData/?$', 'jchem_rest.getChemSpecData'),

)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

