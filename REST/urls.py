from django.conf.urls import url
import cts_rest
import views

urlpatterns = [
    url(r'^$', views.getCTSEndpoints),
    url(r'^swag/?$', views.getSwaggerJsonContent),
    url(r'^docs/?$', cts_rest.showSwaggerPage),

    url(r'^molecule/?$', cts_rest.getChemicalEditorData),
    url(r'^speciation/?$', cts_rest.getChemicalEditorData),

    url(r'^(?P<calc>.*?)/inputs/?$', views.getCalcInputs),
    url(r'^(?P<calc>.*?)/run/?$', views.runCalc),
    url(r'^(?P<endpoint>.*?)/?$', views.getCalcEndpoints),
]
