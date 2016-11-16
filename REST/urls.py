#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
# from django.conf.urls import patterns, include, url
from django.conf.urls import include, url
from REST import views, cts_rest

urlpatterns = [
	url(r'^$', views.getCTSEndpoints),
	url(r'^swag/?$', views.getSwaggerJsonContent),
	url(r'^docs/?$', cts_rest.showSwaggerPage),

	url(r'^molecule/?$', cts_rest.getChemicalEditorData),
	url(r'^speciation/?$', cts_rest.getChemicalSpeciationData),

	# url(r'^hellonode/?$', views.testCTSNodej')

	url(r'^(?P<calc>.*?)/inputs/?$', views.getCalcInputs),
	url(r'^(?P<calc>.*?)/run/?$', views.runCalc),
	url(r'^(?P<endpoint>.*?)/?$', views.getCalcEndpoints),
]

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

