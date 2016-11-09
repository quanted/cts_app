#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
from chemaxon_cts import jchem_rest
# from django.contrib import admin
# admin.autodiscover()
# from REST import cts_rest
import cts_rest


# All view functions here must be in '/views/views.py'
# path: serverLocation/jchem/...
urlpatterns = patterns('REST',
	(r'^/?$', 'views.getCTSEndpoints'),
	(r'^swag/?$', 'views.getSwaggerJsonContent'),
	(r'^docs/?$', 'cts_rest.showSwaggerPage'),

	(r'^molecule/?$', 'cts_rest.getChemicalEditorData'),
	(r'^speciation/?$', 'cts_rest.getChemicalEditorData'),

	# (r'^hellonode/?$', 'views.testCTSNodejs')

	(r'^(?P<calc>.*?)/inputs/?$', 'views.getCalcInputs'),
	(r'^(?P<calc>.*?)/run/?$', 'views.runCalc'),
	(r'^(?P<endpoint>.*?)/?$', 'views.getCalcEndpoints'),
)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

