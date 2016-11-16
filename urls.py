#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
# from django.conf.urls import patterns, include, url
from django.conf.urls import url, include
import REST
from REST import portal, views, urls
import views
from views import batch, ctsGenerateReport, description, input, landing, misc, output
# from django.contrib import admin
# admin.autodiscover()

# The previous urlpatterns is using views as a prefix breaking the use of django apps 
# urlpatterns = patterns('',
#     (r'^cts/wstest/?$', 'REST.portal.test_sockets'),
#     (r'^cts/nodetest/?$', 'REST.views.testCTSNode'),
#     url(r'^cts/portal/?$', 'REST.portal.directAllTraffic'),
#     url(r'^cts/rest/', include('REST.urls'))  # todo: REST --> cts_api?
# )
urlpatterns = [
    url(r'^cts/wstest/?$', REST.portal.test_sockets),
    url(r'^cts/nodetest/?$', REST.views.testCTSNode),
    url(r'^cts/portal/?$', REST.portal.directAllTraffic),
    url(r'^cts/rest/', include(REST.urls))  # todo: REST --> cts_api?
]

# All view functions here must be in '/views/views.py'
# urlpatterns += patterns('',
#     # url(r'^docs/', include('docs.urls')),
#     (r'^$', 'views.landing.ctsLandingPage'),  # Landing page
#     (r'^cts/?$', 'views.landing.ctsLandingPage'),
#     (r'^cts/contact/?$', 'views.misc.fileNotFound'),
#     (r'^cts/fifra/?$', 'views.misc.fileNotFound'),
#     (r'^cts/flame/?$', 'views.misc.fileNotFound'),
#     (r'^cts/ahydrolysis/?$', 'views.misc.displayPDF'),
#     (r'^cts/areduction/?$', 'views.misc.displayPDF'),
#     # (r'^cts/mammet/?$', 'views.misc.fileNotFound'),
#     (r'^cts/guide/?$', 'views.misc.displayPDF'),

#     (r'^cts/(?P<model>.*?)/description/?$', 'views.description.descriptionPage'),
#     (r'^cts/(?P<model>.*?)/input/?$', 'views.input.inputPage'),
#     (r'^cts/(?P<model>.*?)/output/?$', 'views.output.outputPage'),
#     (r'^cts/(?P<model>.*?)/algorithms/?$', 'views.algorithms.algorithmPage'),
#     (r'^cts/(?P<model>.*?)/references/?$', 'views.references.referencesPage'),
#     (r'^cts/(?P<model>.*?)/batch/?$', 'views.batch.batchInputPage'),
#     (r'^cts/(?P<model>.*?)/batchinput/?$', 'views.batch.batchInputPage'),
#     (r'^cts/(?P<model>.*?)/batchoutput/?$', 'views.batch.batchOutputPage'),
#     (r'^cts/(?P<model>.*?)/qaqc/?$', 'views.qaqc.qaqcPage'),
#     (r'^cts/(?P<model>.*?)/history/?$', 'views.misc.fileNotFound'),
#     (r'^cts/.*?/history_revisit\.html$', 'views.history.historyPageRevist'),
#     (r'^cts/(?P<model>.*?)/pdf/?$', 'views.ctsGenerateReport.pdfReceiver'),
#     (r'^cts/(?P<model>.*?)/html/?$', 'views.ctsGenerateReport.htmlReceiver'),
#     (r'^cts/(?P<model>.*?)/csv/?$', 'views.ctsGenerateReport.csvReceiver'),
#     (r'^cts/module/(?P<module>.*?)/?$', 'views.misc.moduleDescriptions'),
#     (r'^cts/docs/?$', 'views.misc.docsRedirect'),
#     (r'^cts/(?P<model>.*?)/?$', 'views.description.descriptionPage'),
# )
urlpatterns += [
    # url(r'^docs/', include('docs.urls')),
    url(r'^$', views.landing.ctsLandingPage),  # Landing page
    url(r'^cts/?$', views.landing.ctsLandingPage),
    url(r'^cts/contact/?$', views.misc.fileNotFound),
    url(r'^cts/fifra/?$', views.misc.fileNotFound),
    url(r'^cts/flame/?$', views.misc.fileNotFound),
    url(r'^cts/ahydrolysis/?$', views.misc.displayPDF),
    url(r'^cts/areduction/?$', views.misc.displayPDF),
    # url(r'^cts/mammet/?$', views.misc.fileNotFound),
    url(r'^cts/guide/?$', views.misc.displayPDF),

    url(r'^cts/(?P<model>.*?)/description/?$', views.description.descriptionPage),
    url(r'^cts/(?P<model>.*?)/input/?$', views.input.inputPage),
    url(r'^cts/(?P<model>.*?)/output/?$', views.output.outputPage),
    # url(r'^cts/(?P<model>.*?)/algorithms/?$', views.algorithms.algorithmPage),
    # url(r'^cts/(?P<model>.*?)/references/?$', views.references.referencesPage),
    url(r'^cts/(?P<model>.*?)/batch/?$', views.batch.batchInputPage),
    url(r'^cts/(?P<model>.*?)/batchinput/?$', views.batch.batchInputPage),
    url(r'^cts/(?P<model>.*?)/batchoutput/?$', views.batch.batchOutputPage),
    # url(r'^cts/(?P<model>.*?)/qaqc/?$', views.qaqc.qaqcPage),
    url(r'^cts/(?P<model>.*?)/history/?$', views.misc.fileNotFound),
    # url(r'^cts/.*?/history_revisit\.html$', views.history.historyPageRevist),
    url(r'^cts/(?P<model>.*?)/pdf/?$', views.ctsGenerateReport.pdfReceiver),
    url(r'^cts/(?P<model>.*?)/html/?$', views.ctsGenerateReport.htmlReceiver),
    url(r'^cts/(?P<model>.*?)/csv/?$', views.ctsGenerateReport.csvReceiver),
    url(r'^cts/module/(?P<module>.*?)/?$', views.misc.moduleDescriptions),
    url(r'^cts/docs/?$', views.misc.docsRedirect),
    url(r'^cts/(?P<model>.*?)/?$', views.description.descriptionPage),
]

# urlpatterns += patterns('', url(r'^/', include('REST.urls')))

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'
# 408 Error view (request timeout)
handler408 = 'views.misc.requestTimeout'

