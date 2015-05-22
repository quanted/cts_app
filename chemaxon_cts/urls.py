#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()


# All view functions here must be in '/views/views.py'
# path: serverLocation/jchem/...
urlpatterns = patterns('REST',
    # url(r'^docs/', include('docs.urls')),
    # (r'^$', 'jchem_rest.doc'),  # Landing page
    (r'^ws/traffic-cop/?$', 'jchem_traffic_cop.directJchemTraffic'),
    (r'^docs/?$', 'jchem_rest.doc'),
    (r'^ws/getChemDetails/?$', 'jchem_rest.getChemDetails'),
    (r'^ws/mrvToSmiles/?$', 'jchem_rest.mrvToSmiles'),
    (r'^ws/getChemSpecData/?$', 'jchem_rest.getChemSpecData'),
    (r'^ws/smilesToImage/?$', 'jchem_rest.smilesToImage'),
    (r'^ws/standardizer/?$', 'jchem_rest.standardizer'),
    (r'^ws/getpchemprops/?$', 'jchem_rest.getpchemprops'),
    # (r'^ws/traffic-cop/?$', 'jchem_rest.trafficCop'),
    # (r'^ws/test-sse/?$', 'jchem_rest.sse_test'), # testing sse in django
    # (r'^ws/test-poll/?$', 'jchem_rest.poll_test') # testing ajax polling
    # (r'^ws/data/?$', 'jchem_rest.poll_test_data')
)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

