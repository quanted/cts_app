#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
from chemaxon_cts import jchem_rest
# from REST.cts_rest import Chemaxon_CTS_REST
# from REST import cts_rest
# from django.contrib import admin
# admin.autodiscover()


# All view functions here must be in '/views/worker.py'
# path: serverLocation/jchem/...
urlpatterns = patterns('chemaxon_cts',
    # url(r'^docs/', include('docs.urls')),
    # (r'^$', 'jchem_rest.doc'),  # Landing page
    (r'/?$', 'jchem_rest.listChemaxonEndpoints'),
    # (r'/?$', 'cts_rest.Chemaxon_CTS_REST().getChemaxonREST'),
    (r'^inputs/?$', 'jchem_rest.chemaxonInputSchema'),
    # (r'^docs/?$', 'jchem_rest.doc'),
    ('getChemDetails/?$', 'jchem_rest.getChemDetails'),
    (r'^convertToSMILES/?$', 'jchem_rest.convertToSMILES'),
    (r'^getChemSpecData/?$', 'jchem_rest.getChemSpecData'),
    (r'^smilesToImage/?$', 'jchem_rest.smilesToImage'),
    # (r'^getpchemprops/?$', 'jchem_rest.getpchemprops'),

    # new api following qed schema:


)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

