#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import include, url
from .views import misc, landing, description, input, output, batch, ctsGenerateReport
# from .cts_api.views import test_ws_page
# from views import history, algorithms, references, qaqc


urlpatterns = [
	# url(r'^/', include('test_cts.urls')),  # Pavan added this to include the test suite django app
	# url(r'^cts/wstest/?$', portal.test_sockets),
	# url(r'^cts/portal/?$', portal.directAllTraffic),
	# url(r'^epi-cts/', include('epi_cts.urls')),  # Pavan added this to include the test suite django app  # REMOVED BY JON DURING DOCKERIZATION
	url(r'^rest/', include('cts_app.cts_api.urls')),
	# url(r'^testing/', include('cts_app.cts_testing.urls'))
	url(r'^testing/', include('cts_app.cts_testing.urls')),

	# url(r'^testws/?$', test_ws_page)
]

# All view functions here must be in '/views/worker.py'
urlpatterns.extend([
	# url(r'^docs/', include('docs.urls')),
	url(r'^$', landing.ctsLandingPage),
	# url(r'^?$', landing.ctsLandingPage),
	url(r'^contact/?$', misc.fileNotFound),
	url(r'^fifra/?$', misc.fileNotFound),
	url(r'^flame/?$', misc.fileNotFound),
	# url(r'^ahydrolysis/?$', misc.displayPDF),
	# url(r'^areduction/?$', misc.displayPDF),
	# url(r'^mammet/?$', misc.fileNotFound),
	# url(r'^guide/?$', misc.displayPDF),
	url(r'^about/(?P<model>.*?)/?$', description.about_page),
	url(r'^flowcharts/(?P<chart>.*?)/?$', description.flowcharts_page),
	url(r'^(?P<model>.*?)/description/?$', description.descriptionPage),
	url(r'^(?P<model>.*?)/input/?$', input.inputPage),
	url(r'^(?P<model>.*?)/output/?$', output.outputPage),
	# url(r'^(?P<model>.*?)/algorithms/?$', algorithms.algorithmPage),
	# url(r'^(?P<model>.*?)/references/?$', references.referencesPage),
	url(r'^(?P<model>.*?)/batch/?$', batch.batchInputPage),
	url(r'^(?P<model>.*?)/batchinput/?$', batch.batchInputPage),
	url(r'^(?P<model>.*?)/batchoutput/?$', batch.batchOutputPage),
	# url(r'^(?P<model>.*?)/qaqc/?$', qaqc.qaqcPage),
	url(r'^(?P<model>.*?)/history/?$', misc.fileNotFound),
	# url(r'^.*?/history_revisit\.html$', history.historyPageRevist),
	url(r'^(?P<model>.*?)/pdf/?$', ctsGenerateReport.pdfReceiver),
	url(r'^(?P<model>.*?)/html/?$', ctsGenerateReport.htmlReceiver),
	url(r'^(?P<model>.*?)/csv/?$', ctsGenerateReport.csvReceiver),
	url(r'^batch/sample/?$', ctsGenerateReport.textReceiver),
	# url(r'^module/(?P<module>.*?)/?$', misc.moduleDescriptions),
	url(r'^docs/?$', misc.docsRedirect),
	url(r'^(?P<model>.*?)/?$', description.descriptionPage),
])

# 404 Error view (file not found)
handler404 = misc.fileNotFound
# 500 Error view (server error)
handler500 = misc.fileNotFound
# 403 Error view (forbidden)
handler403 = misc.fileNotFound
# 408 Error view (request timeout)
handler408 = misc.requestTimeout

