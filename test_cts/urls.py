from django.conf.urls import patterns, url

from test_cts import views

#If you want to use these as stand alone calc APIs enable these urls
urlpatterns = patterns('',
    # url(r'^data/$', views.request_manager)
    #  url(r'^api/(?P<path>.*)$', views.simple_proxy),
    #  url(r'^(?P<model>.*?)/table/?$', views.index, name='index'),
    #  url(r'^calc-kow/$', views.calc_kow)
)
