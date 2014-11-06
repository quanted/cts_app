#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()

# The previous urlpatterns is using views as a prefix breaking the use of django apps 
urlpatterns = patterns('',
    url(r'^test_cts/', include('test_cts.urls'))  # Pavan added this to include the test suite django app
)

# All view functions here must be in '/views/views.py'
urlpatterns += patterns('views',
    # url(r'^docs/', include('docs.urls')),
    (r'^$', 'landing.ctsLandingPage'),  # Landing page
    (r'^cts/?$', 'landing.ctsLandingPage'),
    (r'^cts/contact/?$', 'misc.contact'),
    (r'^cts/(?P<model>.*?)/description/?$', 'description.descriptionPage'),
    (r'^cts/(?P<model>.*?)/input/?$', 'input.inputPage'),
    (r'^cts/(?P<model>.*?)/output/?$', 'output.outputPage'),
    (r'^cts/(?P<model>.*?)/algorithms/?$', 'algorithms.algorithmPage'),
    (r'^cts/(?P<model>.*?)/references/?$', 'references.referencesPage'),
    (r'^cts/(?P<model>.*?)/batchinput/?$', 'batch.batchInputPage'),
    (r'^cts/(?P<model>.*?)/batchoutput/?$', 'batch.batchOutputPage'),
    (r'^cts/(?P<model>.*?)/qaqc/?$', 'qaqc.qaqcPage'),
    (r'^cts/(?P<model>.*?)/history/?$', 'history.historyPage'),
    (r'^cts/.*?/history_revisit\.html$', 'history.historyPageRevist'),
    (r'^cts/(?P<model>.*?)/pdf/?$', 'generateReport.pdfReceiver'),
    (r'^cts/(?P<model>.*?)/html/?$', 'generateReport.htmlReceiver'),
    (r'^cts/docs/?$', 'misc.docsRedirect'),
    (r'^cts/(?P<model>.*?)/?$', 'description.descriptionPage'),
    
    (r'^jchem-cts/', include('REST.urls')),
    # (r'^services/', include('REST.urls')),
)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'
# 408 Error view (request timeout)
handler408 = 'views.misc.requestTimeout'

