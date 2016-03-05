#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
from chemaxon_cts import jchem_rest
# from django.contrib import admin
# admin.autodiscover()
import cts_rest


# All view functions here must be in '/views/views.py'
# path: serverLocation/jchem/...
urlpatterns = patterns('REST',
	(r'^rest/molecule/?$', 'cts_rest.getChemicalEditorData'),
	(r'^rest/speciation/?$', 'cts_rest.getChemicalEditorData'),
)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

