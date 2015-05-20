__author__ = 'KWOLFE'
from django.conf.urls import patterns, url

#from test_cts import views

### If you have not set the TEST_CTS_PROXY_URL variable in settings.py, you're going to be sad.  Here's an example setting you should insert:
#   (in the project's settings.py, you'd add) TEST_CTS_PROXY_URL = "http://10.0.2.2:7080/TEST/"
#   TODO: This is a bit of a hackish solution to the CORS problem, but, for now, it's a solution.
#   For more information: https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS

# urlpatterns = patterns('',
#     url(r'^api/(?P<path>.*)$', views.simple_proxy),
#     url(r'^data/$', views.less_simple_proxy),
#     url(r'^(?P<model>.*?)/table/?$', views.index, name='index'),
#     url(r'^calc-kow/$', views.calc_kow)
#     )