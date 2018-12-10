#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import include, url
from .views import misc, landing, description, input, output, batch, ctsGenerateReport, cts_stress_view
from django.conf import settings


urlpatterns = [
	url(r'^rest/', include('cts_app.cts_api.urls')),
	url(r'^testing/', include('cts_app.cts_testing.urls')),
]

# Adds stress testing URLs if deployed for local dev or on the dev server:
if settings.MACHINE_ID == "developer" or settings.MACHINE_ID == "ord-uber-vm005":
	urlpatterns.extend([
		url(r'^stress/testing/?$', cts_stress_view.cts_stress_page),
		url(r'^stress/html/?$', cts_stress_view.cts_stress_html_download),
	])

# All view functions here must be in '/views/worker.py'
urlpatterns.extend([
	url(r'^$', landing.ctsLandingPage),
	url(r'^contact/?$', misc.fileNotFound),
	url(r'^fifra/?$', misc.fileNotFound),
	url(r'^flame/?$', misc.fileNotFound),
	url(r'^about/(?P<model>.*?)/?$', description.about_page),
	url(r'^flowcharts/(?P<chart>.*?)/?$', description.flowcharts_page),
	url(r'^(?P<model>.*?)/description/?$', description.descriptionPage),
	url(r'^(?P<model>.*?)/input/?$', input.inputPage),
	url(r'^(?P<model>.*?)/output/?$', output.outputPage),
	url(r'^(?P<model>.*?)/batch/?$', batch.batchInputPage),
	url(r'^(?P<model>.*?)/batchinput/?$', batch.batchInputPage),
	url(r'^(?P<model>.*?)/batchoutput/?$', batch.batchOutputPage),
	url(r'^(?P<model>.*?)/history/?$', misc.fileNotFound),
	url(r'^(?P<model>.*?)/pdf/?$', ctsGenerateReport.pdfReceiver),
	url(r'^(?P<model>.*?)/html/?$', ctsGenerateReport.htmlReceiver),
	url(r'^(?P<model>.*?)/csv/?$', ctsGenerateReport.csvReceiver),
	url(r'^batch/sample/?$', ctsGenerateReport.textReceiver),
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

