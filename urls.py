#  https://docs.djangoproject.com/en/1.6/intro/tutorial03/
from django.conf.urls import patterns, include, url
# from django.contrib import admin
# admin.autodiscover()


# All view functions here must be in '/views/views.py'
urlpatterns = patterns('views',
    # url(r'^docs/', include('docs.urls')),
    (r'^$', 'landing.ctsLandingPage'),  # Landing page
    (r'^cts/?$', 'landing.ctsLandingPage'),
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
    # (r'^cts/.*?/przm5_intermediate\.html', 'przm5_intermediate.przm5IntermediatePage'),
    (r'^cts/(?P<model>.*?)/?$', 'description.descriptionPage'),
    # (r'^cts_index\.html$', 'landing.ctsLandingPage'),                        #Legacy links
    # (r'^(?P<model>.*?)_description\.html$', 'description.descriptionPage'),  #Legacy links
    # (r'^(?P<model>.*?)_input\.html$', 'input.inputPage'),                    #Legacy links
    # (r'^(?P<model>.*?)_output\.html$', 'output.outputPage'),                 #Legacy links
    # (r'^(?P<model>.*?)_algorithms\.html$', 'algorithms.algorithmPage'),      #Legacy links
    # (r'^(?P<model>.*?)_references\.html$', 'references.referencesPage'),     #Legacy links
    # (r'^(?P<model>.*?)_batchinput\.html$', 'batch.batchInputPage'),          #Legacy links
    # (r'^(?P<model>.*?)_batchoutput\.html$', 'batch.batchOutputPage'),        #Legacy links
    # (r'^(?P<model>.*?)_qaqc\.html$', 'qaqc.qaqcPage'),                       #Legacy links
    # (r'^(?P<model>.*?)_history\.html$', 'history.historyPage'),              #Legacy links
    # url(r'^admin/', include(admin.site.urls)),
)

# 404 Error view (file not found)
handler404 = 'views.misc.fileNotFound'
# 500 Error view (server error)
handler500 = 'views.misc.fileNotFound'
# 403 Error view (forbidden)
handler403 = 'views.misc.fileNotFound'

