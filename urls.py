#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
import epi_cts
import chemaxon_cts
# from django.contrib import admin
# admin.autodiscover()

# The previous urlpatterns is using views as a prefix breaking the use of django apps 
urlpatterns = patterns('',
    # url(r'^/', include('test_cts.urls')),  # Pavan added this to include the test suite django app
    url(r'^cts/portal/?$', 'REST.portal.directAllTraffic'),
    url(r'^epi-cts/', include('epi_cts.urls')),  # Pavan added this to include the test suite django app
    url(r'^jchem-cts/', include('chemaxon_cts.urls')),
)

# All view functions here must be in '/views/views.py'
urlpatterns += patterns('',
    # url(r'^docs/', include('docs.urls')),
    (r'^$', 'views.landing.ctsLandingPage'),  # Landing page
    (r'^cts/?$', 'views.landing.ctsLandingPage'),
    (r'^cts/contact/?$', 'views.misc.fileNotFound'),
    (r'^cts/fifra/?$', 'views.misc.fileNotFound'),
    (r'^cts/flame/?$', 'views.misc.fileNotFound'),
    # (r'^cts/ahydrolysis/?$', 'views.misc.fileNotFound'), $$$$$$$$$$$$
    (r'^cts/ahydrolysis/?$', 'views.misc.displayPDF'),
    (r'^cts/areduction/?$', 'views.misc.displayPDF'),
    (r'^cts/mammet/?$', 'views.misc.fileNotFound'),
    # (r'^cts/guide/?$', 'views.misc.downloadUserGuide'),
    (r'^cts/guide/?$', 'views.misc.displayPDF'),

    (r'^cts/rest/molecule/?$', 'REST.cts_rest.getChemicalEditorData'),

    (r'^cts/(?P<model>.*?)/description/?$', 'views.description.descriptionPage'),
    (r'^cts/(?P<model>.*?)/input/?$', 'views.input.inputPage'),
    (r'^cts/(?P<model>.*?)/output/?$', 'views.output.outputPage'),
    (r'^cts/(?P<model>.*?)/algorithms/?$', 'views.algorithms.algorithmPage'),
    (r'^cts/(?P<model>.*?)/references/?$', 'views.references.referencesPage'),
    (r'^cts/(?P<model>.*?)/batch/?$', 'views.misc.fileNotFound'),
    (r'^cts/(?P<model>.*?)/batchinput/?$', 'views.batch.batchInputPage'),
    (r'^cts/(?P<model>.*?)/batchoutput/?$', 'views.batch.batchOutputPage'),
    (r'^cts/(?P<model>.*?)/qaqc/?$', 'views.qaqc.qaqcPage'),
    # (r'^cts/(?P<model>.*?)/history/?$', 'views.history.historyPage'),
    (r'^cts/(?P<model>.*?)/history/?$', 'views.misc.fileNotFound'),
    (r'^cts/.*?/history_revisit\.html$', 'views.history.historyPageRevist'),
    (r'^cts/(?P<model>.*?)/pdf/?$', 'views.ctsGenerateReport.pdfReceiver'),
    (r'^cts/(?P<model>.*?)/html/?$', 'views.ctsGenerateReport.htmlReceiver'),
    (r'^cts/(?P<model>.*?)/csv/?$', 'views.ctsGenerateReport.csvReceiver'),
    (r'^cts/module/(?P<module>.*?)/?$', 'views.misc.moduleDescriptions'),
    (r'^cts/docs/?$', 'views.misc.docsRedirect'),
    (r'^cts/(?P<model>.*?)/?$', 'views.description.descriptionPage'),
)

# urlpatterns += patterns('', url(r'^/', include('REST.urls')))

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'
# 408 Error view (request timeout)
handler408 = 'views.misc.requestTimeout'

