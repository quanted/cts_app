#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
# from django.conf.urls import include, url, path
from django.urls import include, path
from cts_app.views import misc, landing, description, input, output, batch, ctsGenerateReport, cts_stress_view, user_comments
from django.conf import settings

import login_middleware


urlpatterns = [
	path('rest/', include('cts_app.cts_api.urls')),
	path('testing/', include('cts_app.cts_testing.urls')),
]

# Adds stress testing URLs if deployed for local dev or on the dev server:
# if settings.MACHINE_ID == "developer":
# 	urlpatterns.extend([
# 		path('stress/testing/', cts_stress_view.cts_stress_page),
# 		path('stress/html/', cts_stress_view.cts_stress_html_download),
# 		path('stress/json/', cts_stress_view.cts_stress_json_download),
# 	])

# All view functions here must be in '/views/worker.py'
urlpatterns.extend([
	path('', landing.ctsLandingPage),
	path('contact/', misc.fileNotFound),
	path('fifra/', misc.fileNotFound),
	path('flame/', misc.fileNotFound),
	path('about/<slug:model>/', description.about_page),
	path('flowcharts/<slug:chart>/', description.flowcharts_page),
	path('forms/contact/', user_comments.handle_contact_post),
	path('<slug:model>/description/', description.descriptionPage),
	path('<slug:model>/input/', input.inputPage),
	path('<slug:model>/output/', output.outputPage),
	path('<slug:model>/batch/', batch.batchInputPage),
	path('<slug:model>/batchinput/', batch.batchInputPage),
	path('<slug:model>/batchoutput/', batch.batchOutputPage),
	path('<slug:model>/history/', misc.fileNotFound),
	# path('<slug:model>/pdf/', ctsGenerateReport.pdfReceiver),
	path('<slug:model>/html/', ctsGenerateReport.htmlReceiver),
	path('<slug:model>/csv/', ctsGenerateReport.csvReceiver),
	path('batch/sample/', ctsGenerateReport.textReceiver),
	path('docs/', misc.docsRedirect),
	path('<slug:model>/', description.descriptionPage),
	path('login/', login_middleware.login),
])

urlpatterns = [path('cts/', include(urlpatterns))]



# 404 Error view (file not found)
handler404 = misc.fileNotFound
# 500 Error view (server error)
handler500 = misc.fileNotFound
# 403 Error view (forbidden)
handler403 = misc.fileNotFound
# 408 Error view (request timeout)
handler408 = misc.requestTimeout

