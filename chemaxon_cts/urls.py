#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
from chemaxon_cts import jchem_rest
# from django.contrib import admin
# admin.autodiscover()


# All view functions here must be in '/views/views.py'
# path: serverLocation/jchem/...
urlpatterns = patterns('chemaxon_cts',
    # url(r'^docs/', include('docs.urls')),
    # (r'^$', 'jchem_rest.doc'),  # Landing page
    (r'^docs/?$', 'jchem_rest.doc'),
    (r'^ws/getChemDetails/?$', 'jchem_rest.getChemDetails'),
    (r'^ws/convertToSMILES/?$', 'jchem_rest.convertToSMILES'),
    (r'^ws/getChemSpecData/?$', 'jchem_rest.getChemSpecData'),
    (r'^ws/smilesToImage/?$', 'jchem_rest.smilesToImage'),
    (r'^ws/getpchemprops/?$', 'jchem_rest.getpchemprops'),
)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

