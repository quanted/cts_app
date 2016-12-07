#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import include, url
from views import misc, landing, description, input, output, batch, ctsGenerateReport
# from views import history, algorithms, references, qaqc


urlpatterns = [
    # url(r'^/', include('test_cts.urls')),  # Pavan added this to include the test suite django app
    # url(r'^cts/wstest/?$', portal.test_sockets),
    # url(r'^cts/portal/?$', portal.directAllTraffic),
    # url(r'^epi-cts/', include('epi_cts.urls')),  # Pavan added this to include the test suite django app  # REMOVED BY JON DURING DOCKERIZATION
    url(r'^cts/rest/', include('cts_api.urls')),
    # url(r'^cts/testing/', include('cts_testing.urls'))
]

# All view functions here must be in '/views/worker.py'
urlpatterns.extend([
    # url(r'^docs/', include('docs.urls')),
    url(r'^$', landing.ctsLandingPage),
    url(r'^cts/?$', landing.ctsLandingPage),
    url(r'^cts/contact/?$', misc.fileNotFound),
    url(r'^cts/fifra/?$', misc.fileNotFound),
    url(r'^cts/flame/?$', misc.fileNotFound),
    url(r'^cts/ahydrolysis/?$', misc.displayPDF),
    url(r'^cts/areduction/?$', misc.displayPDF),
    # url(r'^cts/mammet/?$', misc.fileNotFound),
    url(r'^cts/guide/?$', misc.displayPDF),
    url(r'^cts/(?P<model>.*?)/description/?$', description.descriptionPage),
    url(r'^cts/(?P<model>.*?)/input/?$', input.inputPage),
    url(r'^cts/(?P<model>.*?)/output/?$', output.outputPage),
    # url(r'^cts/(?P<model>.*?)/algorithms/?$', algorithms.algorithmPage),
    # url(r'^cts/(?P<model>.*?)/references/?$', references.referencesPage),
    url(r'^cts/(?P<model>.*?)/batch/?$', batch.batchInputPage),
    url(r'^cts/(?P<model>.*?)/batchinput/?$', batch.batchInputPage),
    url(r'^cts/(?P<model>.*?)/batchoutput/?$', batch.batchOutputPage),
    # url(r'^cts/(?P<model>.*?)/qaqc/?$', qaqc.qaqcPage),
    url(r'^cts/(?P<model>.*?)/history/?$', misc.fileNotFound),
    # url(r'^cts/.*?/history_revisit\.html$', history.historyPageRevist),
    url(r'^cts/(?P<model>.*?)/pdf/?$', ctsGenerateReport.pdfReceiver),
    url(r'^cts/(?P<model>.*?)/html/?$', ctsGenerateReport.htmlReceiver),
    url(r'^cts/(?P<model>.*?)/csv/?$', ctsGenerateReport.csvReceiver),
    url(r'^cts/module/(?P<module>.*?)/?$', misc.moduleDescriptions),
    url(r'^cts/docs/?$', misc.docsRedirect),
    url(r'^cts/(?P<model>.*?)/?$', description.descriptionPage),
])

# 404 Error view (file not found)
handler404 = misc.fileNotFound
# 500 Error view (server error)
handler500 = misc.fileNotFound
# 403 Error view (forbidden)
handler403 = misc.fileNotFound
# 408 Error view (request timeout)
handler408 = misc.requestTimeout

